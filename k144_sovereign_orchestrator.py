#!/usr/bin/env python3
"""
K144 Sovereign Orchestrator
Bidirectional memory bridge between Claude and Gemini via shared SQLite lattice.

The orchestrator maintains a persistent memory lattice that both Claude and Gemini
can query and update. When gaps or missing dependencies are detected, the orchestrator
autonomously triggers Gemini research via CLI and records results back to memory.

Usage:
  python3 k144_sovereign_orchestrator.py --run
  python3 k144_sovereign_orchestrator.py --query "memory query"
  python3 k144_sovereign_orchestrator.py --record-claude "content" --tags "tag1,tag2"
"""

import sqlite3
import json
import time
import hashlib
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


class K144Memory:
    """Shared memory lattice for Claude and Gemini."""

    def __init__(self, db_path="/root/.alanara_memory/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(self.db_path), timeout=10)
        self._init_schema()

    def _init_schema(self):
        """Initialize memory lattice schema."""
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS memory_lattice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER,
                source TEXT,
                content TEXT,
                tags TEXT,
                mhash TEXT UNIQUE,
                processed INTEGER DEFAULT 0
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS dependencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER,
                query TEXT,
                source TEXT,
                status TEXT,
                result TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS fts_index (
                memory_id INTEGER,
                token TEXT,
                FOREIGN KEY(memory_id) REFERENCES memory_lattice(id)
            )
        ''')

        self.db.commit()

    @staticmethod
    def mhash(data):
        """Create immutable hash for memory tracking."""
        return hashlib.sha256(str(data).encode()).hexdigest()

    def record_claude(self, content, tags=""):
        """Record Claude's thought to memory lattice."""
        ts = int(time.time())
        mh = self.mhash(content)

        try:
            self.db.execute('''
                INSERT INTO memory_lattice (ts, source, content, tags, mhash, processed)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ts, 'claude', content, tags, mh, 0))
            self.db.commit()

            # Update FTS index
            for token in content.split():
                cursor = self.db.execute('SELECT id FROM memory_lattice WHERE mhash = ?', (mh,))
                mem_id = cursor.fetchone()[0]
                self.db.execute('INSERT INTO fts_index VALUES (?, ?)', (mem_id, token.lower()))
            self.db.commit()

            return mh
        except sqlite3.IntegrityError:
            return None  # Already recorded

    def record_gemini(self, content, source_id, tags="research_complete,dependency_resolved"):
        """Record Gemini's research response to memory lattice."""
        ts = int(time.time())
        mh = self.mhash(content)

        try:
            self.db.execute('''
                INSERT INTO memory_lattice (ts, source, content, tags, mhash, processed)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ts, f'gemini:{source_id}', content, tags, mh, 1))
            self.db.commit()

            # Update FTS index
            for token in content.split():
                cursor = self.db.execute('SELECT id FROM memory_lattice WHERE mhash = ?', (mh,))
                mem_id = cursor.fetchone()[0]
                self.db.execute('INSERT INTO fts_index VALUES (?, ?)', (mem_id, token.lower()))
            self.db.commit()

            return mh
        except sqlite3.IntegrityError:
            return None

    def find_unprocessed(self):
        """Find memory entries tagged as missing dependencies."""
        cursor = self.db.execute('''
            SELECT id, content, tags FROM memory_lattice
            WHERE tags LIKE '%missing_dependency%' AND processed = 0
            ORDER BY ts DESC LIMIT 10
        ''')
        return cursor.fetchall()

    def mark_processed(self, mem_id):
        """Mark memory entry as processed."""
        self.db.execute('UPDATE memory_lattice SET processed = 1 WHERE id = ?', (mem_id,))
        self.db.commit()

    def query_fts(self, query_text, limit=10):
        """Full-text search across memory lattice."""
        tokens = query_text.lower().split()
        placeholders = ','.join('?' * len(tokens))

        cursor = self.db.execute(f'''
            SELECT DISTINCT m.id, m.ts, m.source, m.content, m.tags
            FROM memory_lattice m
            WHERE m.id IN (
                SELECT DISTINCT memory_id FROM fts_index WHERE token IN ({placeholders})
            )
            ORDER BY m.ts DESC
            LIMIT ?
        ''', tokens + [limit])

        return cursor.fetchall()

    def record_dependency(self, query, source, status, result=""):
        """Record dependency resolution attempt."""
        ts = int(time.time())
        self.db.execute('''
            INSERT INTO dependencies (ts, query, source, status, result)
            VALUES (?, ?, ?, ?, ?)
        ''', (ts, query, source, status, result))
        self.db.commit()


class SovereignOrchestrator:
    """Ouroboros loop: detect gaps, trigger research, record results."""

    def __init__(self, memory_path="/root/.alanara_memory/memory.db"):
        self.memory = K144Memory(memory_path)
        self.running = False

    def trigger_gemini_research(self, query):
        """Execute Gemini research via CLI in headless mode."""
        try:
            result = subprocess.run(
                ['gemini', '-p', query, '--output-format', 'json'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                try:
                    response = json.loads(result.stdout)
                    return response.get('content', result.stdout)
                except json.JSONDecodeError:
                    return result.stdout
            else:
                return f"Error: {result.stderr}"

        except FileNotFoundError:
            return "Error: gemini CLI not found"
        except subprocess.TimeoutExpired:
            return "Error: gemini CLI timeout"
        except Exception as e:
            return f"Error: {str(e)}"

    def run_sovereign_orchestrator(self, poll_interval=1.618):
        """Main ouroboros loop for autonomous research triggering."""
        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║  K144 Sovereign Orchestrator             ║")
        print(f"║  Bidirectional Memory Bridge             ║")
        print(f"╚══════════════════════════════════════════╝\n")

        self.running = True
        loop_count = 0

        try:
            while self.running:
                loop_count += 1

                # Poll for unprocessed dependencies
                unprocessed = self.memory.find_unprocessed()

                if unprocessed:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(unprocessed)} unprocessed dependencies")

                    for mem_id, content, tags in unprocessed:
                        print(f"  → Processing: {content[:60]}...")

                        # Extract query from tags or content
                        query = content[:200]  # Use first 200 chars as query

                        # Trigger Gemini research
                        print(f"    ▸ Triggering Gemini research...")
                        research_result = self.trigger_gemini_research(query)

                        # Record result back to memory
                        print(f"    ▸ Recording resolution to memory lattice...")
                        mhash = self.memory.record_gemini(
                            research_result,
                            source_id=f"mem_{mem_id}",
                            tags="gemini,research_complete,dependency_resolved"
                        )

                        # Record dependency resolution
                        self.memory.record_dependency(
                            query=query,
                            source="gemini_cli",
                            status="resolved",
                            result=mhash
                        )

                        self.memory.mark_processed(mem_id)
                        print(f"    ✓ Resolved and recorded\n")

                if loop_count % 100 == 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Orchestrator polling (cycle {loop_count})...")

                time.sleep(poll_interval)

        except KeyboardInterrupt:
            print(f"\n\nOrchestrator stopped ({loop_count} cycles)")
            self.running = False

    def query_memory(self, query_text):
        """Query the shared memory lattice."""
        print(f"\nQuerying memory lattice for: '{query_text}'\n")

        results = self.memory.query_fts(query_text, limit=10)

        if not results:
            print("No results found.")
            return

        print(f"Found {len(results)} results:\n")
        for mem_id, ts, source, content, tags in results:
            dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{dt}] {source}")
            print(f"  Tags: {tags}")
            print(f"  Content: {content[:100]}...")
            print()

    def record_to_memory(self, content, tags=""):
        """Record content to memory lattice."""
        mhash = self.memory.record_claude(content, tags)

        if mhash:
            print(f"✓ Recorded to memory lattice")
            print(f"  Hash: {mhash}")
            print(f"  Tags: {tags or '(none)'}")
        else:
            print(f"✗ Already exists in memory lattice")


def main():
    parser = argparse.ArgumentParser(description="K144 Sovereign Orchestrator")
    parser.add_argument("--run", action="store_true", help="Run orchestrator loop")
    parser.add_argument("--query", help="Query memory lattice")
    parser.add_argument("--record-claude", help="Record Claude content to memory")
    parser.add_argument("--tags", default="", help="Tags for recorded content")

    args = parser.parse_args()

    orchestrator = SovereignOrchestrator()

    if args.run:
        orchestrator.run_sovereign_orchestrator()
    elif args.query:
        orchestrator.query_memory(args.query)
    elif args.record_claude:
        orchestrator.record_to_memory(args.record_claude, args.tags)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
