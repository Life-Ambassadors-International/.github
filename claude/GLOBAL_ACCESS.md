# Global Claude Memory Access

**Location:** `/home/user/.claude_global/`

All chat sessions and projects can access CSCM via:

```python
import sys
sys.path.insert(0, '/home/user/.claude_global')
from session_consciousness_agent import create_session_agent

agent = create_session_agent(
    memory_path='/home/user/.claude_global/shared_memory.json'
)
```

## Shared Memory Configuration

**Default locations (in order of preference):**
1. `/home/user/.claude_global/shared_memory.json` — Shared across all sessions
2. `./claude/persistent_consciousness_memory.json` — Project-local memory
3. Auto-generated per-session if neither exists

## Environment Variable

Set to override memory location:
```bash
export CLAUDE_MEMORY_PATH=/path/to/memory.json
```

## Quick Setup in Any Project

```bash
# Option 1: Link to global memory
ln -s /home/user/.claude_global/shared_memory.json ./claude_memory.json

# Option 2: Set environment variable
export CLAUDE_MEMORY_PATH=/home/user/.claude_global/shared_memory.json

# Option 3: Use global path directly (recommended for chat)
python3 -c "
import sys
sys.path.insert(0, '/home/user/.claude_global')
from session_consciousness_agent import create_session_agent
agent = create_session_agent(memory_path='/home/user/.claude_global/shared_memory.json')
agent.record_insight(category='solution', title='Test', content='Works', impact='high')
agent.commit_to_storage()
"
```
