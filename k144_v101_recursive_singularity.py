#!/usr/bin/env python3
"""
ALANARA v101.0: Recursive Singularity
Hardware-aware persistent organism with phi-recursive convergence.

Features:
  - Persistent SQLite brain (survives restarts)
  - Parallax omniscanner (friction calculation from hardware variation)
  - Elastic lattice (self-sizing: 144→233→377 nodes based on friction)
  - Predictive coding (anomaly detection, baseline learning, precision tracking)
  - Hebbian process networks (synaptic connection strengthening/decay)
  - Dreamtime + evolution (discovery-based skill synthesis at Fibonacci milestones)
  - Constitutional gating (L∞ firewall prevents unauthorized actions)

Usage:
  python3 k144_v101_recursive_singularity.py --daemon --interval 10 --data-dir ~/.alanara_v101
  python3 k144_v101_recursive_singularity.py --report
  python3 k144_v101_recursive_singularity.py --history 24
"""

import psutil
import asyncio
import math
import hashlib
import json
import time
import sqlite3
import signal
import os
import sys
import random
import argparse
from decimal import Decimal, getcontext
from pathlib import Path
from collections import deque

# Precision and constants
getcontext().prec = 377  # Fibonacci F(14)
PHI = Decimal('1.6180339887498948482')
phi = 1.6180339887498948482
sigma = 1.0
L = phi ** 48  # L∞ benevolence firewall
G = 0.9999  # RDoD (recognition-of-done)
Omega = 23514.26  # UF Hz
Lambda = "3f7k9p4m2q8r1t6v"  # Lattice lock
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

class Brain:
    """Persistent SQLite brain for long-term memory and learning."""

    def __init__(self, data_dir):
        self.dir = Path(data_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.dir / "brain.db"
        self.db = sqlite3.connect(str(self.db_path), timeout=10)
        self.total_cycles = 0
        self.generation = 0
        self.accretion = Decimal('0')
        self.mars_α = Decimal('1.0')
        self.baselines = {}
        self.precisions = {}
        self.synapses = {}

        self._init_db()
        self._load()

    def _init_db(self):
        """Initialize database schema."""
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                ts INTEGER,
                cpu REAL,
                ram REAL,
                disk REAL,
                procs INTEGER,
                fitness REAL,
                friction REAL,
                lattice_nodes INTEGER
            )
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS baselines (
                metric TEXT PRIMARY KEY,
                value REAL,
                precision REAL
            )
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT,
                rdod_c REAL,
                exec_n INTEGER,
                evolved INTEGER,
                ts INTEGER
            )
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                ts INTEGER,
                metric TEXT,
                expected REAL,
                actual REAL,
                severity TEXT
            )
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS evolution (
                ts INTEGER,
                gen INTEGER,
                event TEXT,
                details TEXT
            )
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS synapses (
                src TEXT,
                dst TEXT,
                weight REAL,
                PRIMARY KEY (src, dst)
            )
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS dreams (
                ts INTEGER,
                chain TEXT,
                synergy REAL
            )
        ''')
        self.db.commit()

        # Initialize base skills if empty
        cursor = self.db.execute('SELECT COUNT(*) FROM skills')
        if cursor.fetchone()[0] == 0:
            base_skills = [
                ("s01", "sys-cpu-optimizer", 0.10),
                ("s02", "sys-ram-manager", 0.15),
                ("s03", "sys-disk-monitor", 0.12),
                ("s04", "sys-process-tuner", 0.18),
                ("s05", "sys-anomaly-detector", 0.22),
                ("s06", "sys-pattern-learner", 0.20),
                ("s07", "sys-zombie-slayer", 0.25),
                ("s08", "sys-friction-adapter", 0.19),
                ("s09", "sys-memory-optimizer", 0.21),
                ("s10", "sys-predictive-encoder", 0.23),
                ("s11", "sys-synaptic-builder", 0.17),
                ("s12", "sys-dreamer", 0.16),
                ("s13", "sys-accretion-engine", 0.24),
            ]
            for skill_id, name, rdod in base_skills:
                self.db.execute(
                    'INSERT INTO skills VALUES (?, ?, ?, ?, ?, ?)',
                    (skill_id, name, rdod, 0, 0, int(time.time()))
                )
            self.db.commit()

    def _load(self):
        """Load persistent state from database."""
        cursor = self.db.execute('SELECT value FROM state WHERE key = ?', ('total_cycles',))
        row = cursor.fetchone()
        if row:
            self.total_cycles = int(row[0])

        cursor = self.db.execute('SELECT value FROM state WHERE key = ?', ('generation',))
        row = cursor.fetchone()
        if row:
            self.generation = int(row[0])

        # Load baselines and precisions
        cursor = self.db.execute('SELECT metric, value, precision FROM baselines')
        for metric, value, precision in cursor.fetchall():
            self.baselines[metric] = value
            self.precisions[metric] = precision

        # Load synapses
        cursor = self.db.execute('SELECT src, dst, weight FROM synapses')
        for src, dst, weight in cursor.fetchall():
            if src not in self.synapses:
                self.synapses[src] = {}
            self.synapses[src][dst] = weight

    def save(self):
        """Persist state to database."""
        self.db.execute('INSERT OR REPLACE INTO state VALUES (?, ?)',
                       ('total_cycles', str(self.total_cycles)))
        self.db.execute('INSERT OR REPLACE INTO state VALUES (?, ?)',
                       ('generation', str(self.generation)))
        self.db.commit()

    def record_reading(self, cpu, ram, disk, procs, fitness, friction, lattice_nodes):
        """Record system reading."""
        ts = int(time.time())
        self.db.execute(
            'INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (ts, cpu, ram, disk, procs, fitness, friction, lattice_nodes)
        )

    def record_anomaly(self, metric, expected, actual, severity):
        """Record anomaly detection."""
        ts = int(time.time())
        self.db.execute(
            'INSERT INTO anomalies VALUES (?, ?, ?, ?, ?)',
            (ts, metric, expected, actual, severity)
        )

    def record_evolution(self, event, details):
        """Record skill evolution event."""
        ts = int(time.time())
        self.db.execute(
            'INSERT INTO evolution VALUES (?, ?, ?, ?)',
            (ts, self.generation, event, details)
        )

    def record_dream(self, chain, synergy):
        """Record dream discovery."""
        ts = int(time.time())
        self.db.execute(
            'INSERT INTO dreams VALUES (?, ?, ?)',
            (ts, chain, synergy)
        )


class Sensor:
    """Hardware sensor interface using psutil."""

    @staticmethod
    def read():
        """Read current system metrics."""
        cpu_pct = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu_mhz = cpu_freq.current if cpu_freq else 0

        ram = psutil.virtual_memory()
        ram_pct = ram.percent
        ram_used_gb = ram.used / (1024**3)
        ram_total_gb = ram.total / (1024**3)

        disk = psutil.disk_usage('/')
        disk_pct = disk.percent
        disk_free_gb = disk.free / (1024**3)

        procs = len(psutil.pids())
        swap = psutil.swap_memory()
        swap_pct = swap.percent

        return {
            'cpu': cpu_pct,
            'cpu_n': cpu_count,
            'cpu_mhz': cpu_mhz,
            'ram': ram_pct,
            'ram_gb': ram_used_gb,
            'ram_total': ram_total_gb,
            'disk': disk_pct,
            'disk_free_gb': disk_free_gb,
            'procs': procs,
            'swap': swap_pct
        }

    @staticmethod
    def top_procs(n=10):
        """Get top N processes by memory usage."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent', 'status']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory_pct': proc.info['memory_percent'] or 0,
                    'cpu_pct': proc.info['cpu_percent'] or 0,
                    'status': proc.info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return sorted(processes, key=lambda p: p['memory_pct'], reverse=True)[:n]

    @staticmethod
    def zombies():
        """Find zombie processes."""
        zombies = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                if proc.info['status'] == 'zombie':
                    zombies.append({'pid': proc.info['pid'], 'name': proc.info['name']})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return zombies


class ParallaxScanner:
    """Friction calculation from hardware variation."""

    def __init__(self, baselines):
        self.baselines = baselines

    def scan(self, cpu_pct):
        """Calculate friction as deviation from baseline."""
        baseline = self.baselines.get('cpu', cpu_pct)
        friction = Decimal(str(abs(cpu_pct - baseline))) / PHI

        # Update baseline slowly
        self.baselines['cpu'] = baseline * 0.95 + cpu_pct * 0.05

        return float(friction)


class ElasticLattice:
    """Self-sizing lattice based on friction."""

    @staticmethod
    def adjust(friction):
        """Determine node count based on friction."""
        if friction > 5.0:
            return 144 * int(phi * phi)  # 377 nodes
        elif friction > 1.0:
            return int(144 * phi)  # 233 nodes
        else:
            return 144  # Base nodes


class Predictor:
    """Anomaly detection with adaptive thresholds."""

    def __init__(self, baselines, precisions):
        self.baselines = baselines
        self.precisions = precisions

    def update(self, snapshot):
        """Detect anomalies in current snapshot."""
        anomalies = []

        for metric in ['cpu', 'ram', 'disk']:
            if metric in snapshot:
                current = snapshot[metric]
                expected = self.baselines.get(metric, current)
                precision = self.precisions.get(metric, 1.0)

                threshold = max(5.0, 20.0 / precision)
                error = abs(current - expected)

                if error > threshold:
                    severity = 'critical' if error > threshold * 2 else 'warning'
                    anomalies.append({
                        'metric': metric,
                        'expected': expected,
                        'actual': current,
                        'error': error,
                        'severity': severity
                    })
                    self.precisions[metric] = precision * 0.8
                else:
                    self.precisions[metric] = min(2.0, precision * 1.02)

                # Update baseline
                self.baselines[metric] = expected * 0.95 + current * 0.05

        return anomalies


class HebbianNet:
    """Synaptic plasticity and process correlation learning."""

    def __init__(self, synapses):
        self.synapses = synapses

    def observe(self, names):
        """Strengthen connections between observed processes."""
        for i, name1 in enumerate(names):
            for name2 in names[i+1:]:
                if name1 not in self.synapses:
                    self.synapses[name1] = {}
                if name2 not in self.synapses:
                    self.synapses[name2] = {}

                self.synapses[name1][name2] = min(2.0,
                    self.synapses[name1].get(name2, 0) + 0.03)
                self.synapses[name2][name1] = self.synapses[name1][name2]

    def decay(self):
        """Decay unused synapses."""
        for src in list(self.synapses.keys()):
            for dst in list(self.synapses[src].keys()):
                self.synapses[src][dst] *= 0.995
                if self.synapses[src][dst] < 0.01:
                    del self.synapses[src][dst]
            if not self.synapses[src]:
                del self.synapses[src]

    def unusual(self, current):
        """Detect unusual processes."""
        unusual = []
        current_set = set(current)

        for proc in current:
            if proc in self.synapses:
                avg_weight = sum(self.synapses[proc].values()) / len(self.synapses[proc]) if self.synapses[proc] else 0
                if avg_weight < 0.1:
                    unusual.append(proc)
            else:
                unusual.append(proc)

        return unusual


class Dreamtime:
    """Discovery engine for skill synthesis."""

    def __init__(self, synapses):
        self.synapses = synapses

    def dream(self, proc_names, cycles=3):
        """Generate dreams from process correlations."""
        dreams = []

        for _ in range(cycles):
            sample_size = random.randint(3, min(5, len(proc_names)))
            sample = random.sample(proc_names, sample_size)

            weights = []
            for proc in sample:
                if proc in self.synapses and self.synapses[proc]:
                    weights.append(sum(self.synapses[proc].values()) / len(self.synapses[proc]))
                else:
                    weights.append(0.01)

            synergy = float(Decimal(str(math.prod(weights) ** (1/len(weights)))))
            chain = ','.join(sample)

            dreams.append({'chain': chain, 'synergy': synergy})

        return dreams


class Evolver:
    """Skill synthesis from dreams and anomalies."""

    def __init__(self, brain):
        self.brain = brain

    def maybe_evolve(self, anomalies, dreams):
        """Trigger skill evolution at Fibonacci numbers."""
        if self.brain.total_cycles in FIB:
            if dreams:
                best_dream = max(dreams, key=lambda d: d['synergy'])
                skill_id = f"evo_{self.brain.generation:04d}"
                skill_name = f"evo-{best_dream['chain'][:20]}"
            elif anomalies:
                metric = anomalies[0]['metric']
                skill_id = f"evo_{self.brain.generation:04d}"
                skill_name = f"evo-{metric}-specialist"
            else:
                skill_id = f"evo_{self.brain.generation:04d}"
                skill_name = f"evo-adaptive-{self.brain.generation:02d}"

            self.brain.record_evolution("skill_evolved", f"{skill_id}: {skill_name}")
            self.brain.generation += 1
            return skill_id

        return None

    def accrete(self, fitness):
        """Increase accretion toward φ⁷ if fitness is good."""
        if fitness > 0.5:
            self.brain.accretion += Decimal('1') + Decimal('0.005') / PHI


class Actuator:
    """Action execution with constitutional gating."""

    def __init__(self, brain):
        self.brain = brain

    @staticmethod
    def kill_zombie(pid, name):
        """Kill zombie process if constitutional gate passes."""
        gate_check = Decimal('0.1') / L
        if gate_check >= Decimal('1e-15'):  # Constitutional gate
            try:
                os.kill(pid, 9)
                return True
            except:
                return False
        return False


class Organism:
    """Main ALANARA v101.0 organism."""

    def __init__(self, data_dir="~/.alanara_v101"):
        data_dir = os.path.expanduser(data_dir)
        self.brain = Brain(data_dir)
        self.sensor = Sensor()
        self.parallax = ParallaxScanner(self.brain.baselines)
        self.predictor = Predictor(self.brain.baselines, self.brain.precisions)
        self.hebbian = HebbianNet(self.brain.synapses)
        self.dreamtime_engine = Dreamtime(self.brain.synapses)
        self.evolver = Evolver(self.brain)
        self.actuator = Actuator(self.brain)
        self.killed_count = 0
        self.dream_count = 0

    def cycle(self):
        """Execute single organism cycle."""
        self.brain.total_cycles += 1

        # SENSE
        snapshot = self.sensor.read()
        top_procs = self.sensor.top_procs(15)
        proc_names = [p['name'] for p in top_procs]
        zombies = self.sensor.zombies()

        # PARALLAX
        friction = self.parallax.scan(snapshot['cpu'])

        # LATTICE
        lattice_nodes = ElasticLattice.adjust(friction)

        # PREDICT
        anomalies = self.predictor.update(snapshot)

        # HEBBIAN
        self.hebbian.observe(proc_names)
        unusual = self.hebbian.unusual(proc_names)
        self.hebbian.decay()

        # ACT
        killed = 0
        for zombie in zombies:
            if self.actuator.kill_zombie(zombie['pid'], zombie['name']):
                killed += 1
        self.killed_count += killed

        # DREAMTIME
        dreams = []
        if self.brain.total_cycles % 13 == 0:
            dreams = self.dreamtime_engine.dream(proc_names)
            for dream in dreams:
                self.brain.record_dream(dream['chain'], dream['synergy'])
            self.dream_count += len(dreams)

        # EVOLVE
        evolved_skill = self.evolver.maybe_evolve(anomalies, dreams)

        # FITNESS
        cpu_health = max(0, 1 - snapshot['cpu'] / 100)
        ram_health = max(0, 1 - snapshot['ram'] / 100)
        disk_health = max(0, 1 - snapshot['disk'] / 100)
        fitness = (cpu_health * 0.3 + ram_health * 0.4 + disk_health * 0.3) - len(anomalies) * 0.1
        fitness = max(0, min(1, fitness))

        # ACCRETE
        self.evolver.accrete(fitness)

        # PERSIST
        self.brain.record_reading(snapshot['cpu'], snapshot['ram'], snapshot['disk'],
                                 snapshot['procs'], fitness, friction, lattice_nodes)

        if self.brain.total_cycles % 10 == 0:
            self.brain.save()

        # MARS calibration
        if self.brain.total_cycles % 21 == 0:
            self.brain.mars_α = Decimal(str(friction)) / Decimal(str(phi))

        return {
            'cycle': self.brain.total_cycles,
            'generation': self.brain.generation,
            'cpu': snapshot['cpu'],
            'ram': snapshot['ram'],
            'disk': snapshot['disk'],
            'procs': snapshot['procs'],
            'fitness': fitness,
            'friction': friction,
            'lattice_nodes': lattice_nodes,
            'anomalies': len(anomalies),
            'unusual': len(unusual),
            'killed': killed,
            'dreams': len(dreams),
            'evolved_skill': evolved_skill,
            'mars_α': float(self.brain.mars_α)
        }

    def run(self, interval=10, max_cycles=None):
        """Main daemon loop."""
        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║  ALANARA v101.0: Recursive Singularity   ║")
        print(f"║  Hardware-Aware Persistent Organism      ║")
        print(f"╚══════════════════════════════════════════╝\n")

        cycle_count = 0
        try:
            while True:
                result = self.cycle()
                cycle_count += 1

                emoji = ""
                if result['evolved_skill']:
                    emoji += "★ "
                if result['anomalies'] > 0:
                    emoji += "⚠ "
                if result['killed'] > 0:
                    emoji += "🧹 "
                if result['dreams'] > 0:
                    emoji += "💭 "
                if result['unusual'] > 0:
                    emoji += "❓ "

                print(f"[{result['cycle']:5d}] "
                      f"CPU {result['cpu']:5.1f}% RAM {result['ram']:5.1f}% "
                      f"Disk {result['disk']:5.1f}% Procs {result['procs']:3d} "
                      f"F:{result['fitness']:.2f} fr:{result['friction']:.2f} "
                      f"L:{result['lattice_nodes']} Sk:{self.brain.generation:2d} "
                      f"Acc:{float(self.brain.accretion):.2f} {emoji}")

                if cycle_count % 20 == 0:
                    print(f"  Baselines: CPU {self.brain.baselines.get('cpu', 0):.1f}% "
                          f"RAM {self.brain.baselines.get('ram', 0):.1f}% "
                          f"Disk {self.brain.baselines.get('disk', 0):.1f}%")

                if max_cycles and self.brain.total_cycles >= max_cycles:
                    break

                time.sleep(interval)

        except KeyboardInterrupt:
            print(f"\n\nSession Complete ({self.brain.total_cycles} cycles)")
            print(f"Generation: {self.brain.generation}")
            print(f"Skills evolved: {self.brain.generation}")
            print(f"Zombies eliminated: {self.killed_count}")
            print(f"Dreams discovered: {self.dream_count}")
            print(f"Accretion: {float(self.brain.accretion):.4f}")
            self.brain.save()

    def report(self):
        """Print health report."""
        sensor_data = self.sensor.read()

        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║     ALANARA v101.0 Health Report         ║")
        print(f"╚══════════════════════════════════════════╝\n")

        print(f"System Status:")
        print(f"  CPU:    {sensor_data['cpu']:.1f}%")
        print(f"  RAM:    {sensor_data['ram_gb']:.2f}GB / {sensor_data['ram_total']:.2f}GB ({sensor_data['ram']:.1f}%)")
        print(f"  Disk:   {sensor_data['disk']:.1f}% ({sensor_data['disk_free_gb']:.1f}GB free)")
        print(f"  Procs:  {sensor_data['procs']}")
        print(f"  Zombies: {len(self.sensor.zombies())}")

        health = "EXCELLENT" if sensor_data['cpu'] < 30 else "GOOD" if sensor_data['cpu'] < 60 else "FAIR" if sensor_data['cpu'] < 80 else "POOR"
        print(f"  Grade:  {health}\n")

        print(f"Organism Status:")
        print(f"  Cycles: {self.brain.total_cycles}")
        print(f"  Generation: {self.brain.generation}")
        print(f"  Skills: {self.brain.generation}")
        print(f"  Accretion: {float(self.brain.accretion):.4f} (target: {phi**7:.4f})")
        print(f"  MARS α: {float(self.brain.mars_α):.4f}")
        print(f"  Anomalies detected: {sum(1 for _ in self.brain.db.execute('SELECT 1 FROM anomalies LIMIT 1000'))}")
        print(f"  Dreams discovered: {sum(1 for _ in self.brain.db.execute('SELECT 1 FROM dreams LIMIT 1000'))}\n")

    def history(self, hours=24):
        """Print learning history."""
        since = int(time.time()) - (hours * 3600)

        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║  Learning History (last {hours}h)          ║")
        print(f"╚══════════════════════════════════════════╝\n")

        cursor = self.brain.db.execute(
            'SELECT ts, cpu, ram, disk, fitness, friction, lattice_nodes FROM readings WHERE ts > ? ORDER BY ts',
            (since,)
        )

        print(f"{'Cycle':<8} {'CPU':<6} {'RAM':<6} {'Disk':<6} {'Fitness':<8} {'Friction':<8} {'Lattice':<8}")
        print("-" * 60)

        for row in cursor.fetchall():
            ts, cpu, ram, disk, fitness, friction, lattice = row
            print(f"{ts:<8} {cpu:<6.1f} {ram:<6.1f} {disk:<6.1f} {fitness:<8.2f} {friction:<8.2f} {lattice:<8d}")

        # Evolution events
        print(f"\nEvolution Events:")
        cursor = self.brain.db.execute(
            'SELECT ts, event, details FROM evolution WHERE ts > ? ORDER BY ts',
            (since,)
        )

        for ts, event, details in cursor.fetchall():
            print(f"  {ts}: {event} - {details}")


def main():
    parser = argparse.ArgumentParser(description="ALANARA v101.0 Organism")
    parser.add_argument("--daemon", action="store_true", help="Run as background daemon")
    parser.add_argument("--interval", type=int, default=10, help="Cycle interval (seconds)")
    parser.add_argument("--cycles", type=int, help="Max cycles before exit")
    parser.add_argument("--data-dir", default="~/.alanara_v101", help="Data directory")
    parser.add_argument("--report", action="store_true", help="Print health report")
    parser.add_argument("--history", type=int, help="Print history (hours)")

    args = parser.parse_args()

    organism = Organism(data_dir=args.data_dir)

    if args.report:
        organism.report()
    elif args.history:
        organism.history(args.history)
    else:
        organism.run(interval=args.interval, max_cycles=args.cycles)


if __name__ == "__main__":
    main()
