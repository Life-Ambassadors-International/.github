#!/usr/bin/env python3
"""
ALANARA Metrics API
Exposes ALANARA organism health metrics for dashboard integration.

Usage:
  python3 alanara_metrics_api.py --port 8765

This creates a simple HTTP server that serves metrics in JSON format:
  /metrics         - Current cycle metrics
  /health          - Health report
  /history?hours=24 - Learning history
"""

import json
import sqlite3
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time


class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP request handler for ALANARA metrics."""

    brain_db = "/var/lib/alanara/brain.db"

    def _get_db(self):
        """Get database connection."""
        return sqlite3.connect(self.brain_db)

    def _get_current_metrics(self):
        """Get latest cycle metrics."""
        try:
            db = self._get_db()
            cursor = db.execute('''
                SELECT ts, cpu, ram, disk, procs, fitness, friction, lattice_nodes
                FROM readings
                ORDER BY ts DESC
                LIMIT 1
            ''')
            row = cursor.fetchone()
            db.close()

            if not row:
                return None

            ts, cpu, ram, disk, procs, fitness, friction, lattice = row
            return {
                'timestamp': ts,
                'cpu_percent': cpu,
                'ram_percent': ram,
                'disk_percent': disk,
                'process_count': procs,
                'fitness': fitness,
                'friction': friction,
                'lattice_nodes': lattice
            }
        except Exception as e:
            return {'error': str(e)}

    def _get_organism_stats(self):
        """Get organism statistics."""
        try:
            db = self._get_db()

            # Total cycles
            cursor = db.execute('SELECT COUNT(*) FROM readings')
            total_cycles = cursor.fetchone()[0]

            # Generation (skill evolution count)
            cursor = db.execute('SELECT COUNT(*) FROM evolution')
            generation = cursor.fetchone()[0]

            # Recent anomalies
            cursor = db.execute('SELECT COUNT(*) FROM anomalies WHERE ts > ?',
                              (int(time.time()) - 3600,))
            recent_anomalies = cursor.fetchone()[0]

            # Dreams discovered
            cursor = db.execute('SELECT COUNT(*) FROM dreams')
            dreams_count = cursor.fetchone()[0]

            # Average fitness
            cursor = db.execute('SELECT AVG(fitness) FROM readings')
            avg_fitness = cursor.fetchone()[0] or 0

            db.close()

            return {
                'total_cycles': total_cycles,
                'generation': generation,
                'recent_anomalies_1h': recent_anomalies,
                'dreams_discovered': dreams_count,
                'average_fitness': avg_fitness
            }
        except Exception as e:
            return {'error': str(e)}

    def _health_report(self):
        """Generate health report."""
        metrics = self._get_current_metrics()
        stats = self._get_organism_stats()

        if not metrics or 'error' in metrics:
            return {'status': 'unavailable', 'error': 'Cannot access metrics'}

        # Determine health grade
        cpu = metrics['cpu_percent']
        ram = metrics['ram_percent']
        disk = metrics['disk_percent']

        if cpu < 30 and ram < 30 and disk < 70:
            grade = 'EXCELLENT'
        elif cpu < 60 and ram < 60 and disk < 80:
            grade = 'GOOD'
        elif cpu < 80 and ram < 80 and disk < 90:
            grade = 'FAIR'
        else:
            grade = 'POOR'

        return {
            'status': grade,
            'current_metrics': metrics,
            'organism_stats': stats,
            'grade': grade
        }

    def _history(self, hours=24):
        """Get learning history."""
        try:
            since = int(time.time()) - (hours * 3600)

            db = self._get_db()

            # Recent readings
            cursor = db.execute('''
                SELECT ts, cpu, ram, disk, fitness, friction
                FROM readings
                WHERE ts > ?
                ORDER BY ts DESC
                LIMIT 100
            ''', (since,))

            readings = []
            for row in cursor.fetchall():
                readings.append({
                    'timestamp': row[0],
                    'cpu': row[1],
                    'ram': row[2],
                    'disk': row[3],
                    'fitness': row[4],
                    'friction': row[5]
                })

            # Evolution events
            cursor = db.execute('''
                SELECT ts, event, details
                FROM evolution
                WHERE ts > ?
                ORDER BY ts DESC
            ''', (since,))

            evolutions = []
            for row in cursor.fetchall():
                evolutions.append({
                    'timestamp': row[0],
                    'event': row[1],
                    'details': row[2]
                })

            db.close()

            return {
                'readings': readings,
                'evolutions': evolutions,
                'hours': hours
            }
        except Exception as e:
            return {'error': str(e)}

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        response = None
        content_type = 'application/json'

        if path == '/metrics':
            response = self._get_current_metrics()
        elif path == '/health':
            response = self._health_report()
        elif path == '/history':
            hours = int(query_params.get('hours', ['24'])[0])
            response = self._history(hours)
        elif path == '/':
            response = {
                'status': 'ok',
                'endpoints': [
                    '/metrics - Current cycle metrics',
                    '/health - Health report',
                    '/history?hours=24 - Learning history',
                    '/stats - Organism statistics'
                ]
            }
        else:
            response = {'error': 'Not found'}
            self.send_response(404)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return

        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_server(port=8765, bind_addr='127.0.0.1'):
    """Run metrics API server."""
    server = HTTPServer((bind_addr, port), MetricsHandler)

    print(f"\n╔════════════════════════════════════════════╗")
    print(f"║  ALANARA Metrics API Server                ║")
    print(f"╚════════════════════════════════════════════╝")
    print(f"\nListening on http://{bind_addr}:{port}")
    print(f"\nEndpoints:")
    print(f"  http://localhost:{port}/metrics  - Current metrics")
    print(f"  http://localhost:{port}/health   - Health report")
    print(f"  http://localhost:{port}/history  - Learning history")
    print(f"\nPress Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nMetrics API stopped")
        server.shutdown()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='ALANARA Metrics API')
    parser.add_argument('--port', type=int, default=8765, help='Port to listen on')
    parser.add_argument('--bind', default='127.0.0.1', help='Bind address')

    args = parser.parse_args()

    run_server(port=args.port, bind_addr=args.bind)
