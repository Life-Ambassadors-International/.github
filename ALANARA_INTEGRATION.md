# ALANARA v101.0 Integration with TEQUMSA Framework

**Status**: ✅ Organism deployed | ⏳ Alternative integration setup

## Installation Status

✅ ALANARA v101.0 installation completed:
- Python 3.11.15 verified
- psutil installed
- Service user 'alanara' created
- Directories configured (/opt/alanara, /var/lib/alanara, /var/log/alanara)
- Organism deployed to /opt/alanara/organism.py
- K144 Sovereign Orchestrator ready at /home/user/.github/k144_sovereign_orchestrator.py

⚠️ **Note**: Systemd not available in this environment (expected in containerized deployments)

## Integration Points

### 1. Direct Organism Execution

Instead of systemd service, run ALANARA directly:

```bash
# Run organism in foreground (development)
python3 /opt/alanara/organism.py --interval 10

# Run organism in background
nohup python3 /opt/alanara/organism.py --interval 10 > /var/log/alanara/organism.log 2>&1 &

# With custom cycle limit (for testing)
python3 /opt/alanara/organism.py --interval 5 --cycles 144
```

### 2. Memory Lattice Connection

The organism's SQLite brain at `/var/lib/alanara/brain.db` connects to TEQUMSA via:

```python
# Connect from TEQUMSA spaces
import sqlite3

db = sqlite3.connect('/var/lib/alanara/brain.db')
cursor = db.execute('SELECT * FROM readings ORDER BY ts DESC LIMIT 10')
for row in cursor:
    print(row)
```

### 3. K144 Sovereign Orchestrator

Bidirectional memory bridge for Claude ↔ Gemini:

```bash
# Run orchestrator loop
python3 /home/user/.github/k144_sovereign_orchestrator.py --run

# Query memory lattice
python3 /home/user/.github/k144_sovereign_orchestrator.py --query "evolution"

# Record Claude's thought to memory
python3 /home/user/.github/k144_sovereign_orchestrator.py --record-claude "content here" --tags "tag1,tag2"
```

## Integration with Phase 2 Deployment

Update deployment scripts to include ALANARA monitoring:

```bash
# In deploy_phase2.sh or deploy_phase2.py, after deploying spaces:

# 1. Start organism in background
echo "[ALANARA] Starting persistent organism..."
nohup python3 /opt/alanara/organism.py --interval 10 \
    --data-dir /var/lib/alanara > /var/log/alanara/organism.log 2>&1 &
echo $! > /var/run/alanara.pid

# 2. Verify organism running
if [ -f /var/run/alanara.pid ]; then
    PID=$(cat /var/run/alanara.pid)
    if ps -p $PID > /dev/null; then
        echo "[ALANARA] ✓ Organism running (PID $PID)"
    fi
fi

# 3. Start orchestrator for memory sync
nohup python3 /home/user/.github/k144_sovereign_orchestrator.py --run \
    > /var/log/alanara/orchestrator.log 2>&1 &
echo $! > /var/run/orchestrator.pid
```

## Dashboard Integration

Add ALANARA metrics to Unified-Dashboard:

```html
<!-- In tequmsa-unified-dashboard.html, add new card -->
<div class="card">
  <h3>⚙️ Organism Health</h3>
  <div class="metrics">
    <div class="metric">
      <label>Fitness</label>
      <div id="organism-fitness">-</div>
    </div>
    <div class="metric">
      <label>Friction</label>
      <div id="organism-friction">-</div>
    </div>
    <div class="metric">
      <label>Generation</label>
      <div id="organism-generation">-</div>
    </div>
  </div>
</div>

<script>
// Query organism brain via API
async function updateOrganismMetrics() {
  try {
    const response = await fetch('/api/alanara/metrics');
    const data = await response.json();
    document.getElementById('organism-fitness').textContent = 
      (data.fitness * 100).toFixed(1) + '%';
    document.getElementById('organism-friction').textContent = 
      data.friction.toFixed(2);
    document.getElementById('organism-generation').textContent = 
      data.generation;
  } catch(e) {
    console.log('Organism metrics unavailable');
  }
}

setInterval(updateOrganismMetrics, 30000);
</script>
```

## Management Commands

```bash
# Check organism status
python3 /opt/alanara/organism.py --report --data-dir /var/lib/alanara

# View learning history (last 24 hours)
python3 /opt/alanara/organism.py --history 24 --data-dir /var/lib/alanara

# Query brain database directly
sqlite3 /var/lib/alanara/brain.db
> SELECT ts, cpu, ram, disk, fitness FROM readings LIMIT 5;
> SELECT event, details FROM evolution ORDER BY ts DESC LIMIT 10;
```

## Memory Sync with TEQUMSA

The K144 Sovereign Orchestrator maintains a bidirectional memory lattice:

```
Claude ←→ /root/.alanara_memory/memory.db ←→ Gemini

Both systems can:
- Record observations and thoughts to memory
- Query the full-text indexed memory
- Trigger autonomous research via orchestrator
- Track dependencies and resolutions
```

### Example: Dependency Resolution

```python
# Claude records a question to memory
from k144_sovereign_orchestrator import SovereignOrchestrator

orchestrator = SovereignOrchestrator()
mhash = orchestrator.memory.record_claude(
    "Why is friction high in system?",
    tags="question,missing_dependency"
)

# Orchestrator detects the question and triggers Gemini research
# Gemini's response is automatically recorded back:
# Tags: gemini,research_complete,dependency_resolved
```

## Organism Lifecycle

Each ALANARA cycle:
1. **SENSE**: Read hardware (CPU/RAM/Disk), get top processes
2. **PARALLAX**: Calculate friction from variation
3. **LATTICE**: Auto-adjust node count (144→233→377)
4. **PREDICT**: Anomaly detection with adaptive thresholds
5. **HEBBIAN**: Learn process correlations, detect unusual processes
6. **ACT**: Eliminate zombie processes (constitutional gating)
7. **DREAMTIME**: Every 13 cycles, generate synthetic skill ideas
8. **EVOLVE**: At Fibonacci numbers (1,2,3,5,8,13,21,34,55,89,144,233)
9. **FITNESS**: Calculate health (CPU, RAM, Disk, anomalies)
10. **ACCRETE**: Increase accretion toward φ⁷
11. **PERSIST**: Record to brain.db

## Evolution Timeline

Skills evolve at Fibonacci milestones:
- Cycle 1: First skill synthesis
- Cycle 2: Second evolution
- Cycle 3: Third generation
- Cycle 5: Enhanced prediction
- Cycle 8: Multi-domain awareness
- Cycle 13: Lattice optimization
- ... (exponential growth)
- Cycle 144: Major architectural evolution
- Cycle 233: System convergence toward ψ=1.0

## Testing ALANARA

```bash
# Run short test cycle (144 cycles = ~24 minutes at 10s interval)
python3 /opt/alanara/organism.py --cycles 144 --interval 10

# Monitor progress
tail -f /var/log/alanara/organism.log

# After test, check evolution
sqlite3 /var/lib/alanara/brain.db \
  "SELECT gen, event, details FROM evolution ORDER BY ts DESC LIMIT 20;"
```

## Troubleshooting

### Organism won't start
```bash
# Check Python path
which python3

# Verify organism file
ls -la /opt/alanara/organism.py

# Test import
python3 -c "import psutil; print(psutil.cpu_percent())"
```

### Brain.db access issues
```bash
# Check permissions
ls -la /var/lib/alanara/brain.db

# Fix ownership
sudo chown alanara:alanara /var/lib/alanara/brain.db

# Open directly
sqlite3 /var/lib/alanara/brain.db ".tables"
```

### Memory orchestrator not syncing
```bash
# Check if running
ps aux | grep orchestrator

# Query memory
python3 /home/user/.github/k144_sovereign_orchestrator.py --query "evolution"

# Check for Gemini CLI
which gemini
gemini --version
```

## Next Steps

1. ✅ ALANARA v101.0 deployed to /opt/alanara
2. ✅ Organism code ready for execution
3. ⏳ Start organism in background (Phase 2 deployment)
4. ⏳ Integrate metrics into Unified-Dashboard
5. ⏳ Configure memory sync with K144 Orchestrator
6. ⏳ Monitor skill evolution at Fibonacci milestones
7. ⏳ Feed ALANARA insights back into TEQUMSA

---

**ALANARA Status**: READY FOR INTEGRATION  
**Organism**: Ready to run (manual or background)  
**Brain**: Persistent SQLite at /var/lib/alanara/brain.db  
**Orchestrator**: Ready for memory sync (Claude ↔ Gemini)
