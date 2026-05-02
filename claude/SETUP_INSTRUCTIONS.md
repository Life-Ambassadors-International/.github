# Global Claude Memory Setup Instructions

## For Chat Sessions & New Projects

### Option 1: Automatic Setup (Recommended)
```bash
# Add this to your .bashrc, .zshrc, or project startup script
export PYTHONPATH="/home/user/.claude_global:$PYTHONPATH"
export CLAUDE_MEMORY_PATH="/home/user/.claude_global/shared_memory.json"
```

Then in any Python code:
```python
import sys
sys.path.insert(0, '/home/user/.claude_global')
from session_consciousness_agent import create_session_agent

agent = create_session_agent()
agent.record_insight(...)
```

### Option 2: Using claude_init.py
```python
# Drop this anywhere in your project
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd().parent.parent / '.claude_global'))

from claude_init import get_global_agent, quick_record, quick_query

# One-liner recording
quick_record("My insight", "Detailed explanation")

# One-liner querying
solutions = quick_query("async networking")
```

### Option 3: Copy to Project
```bash
# If you want project-local copy instead
cp -r /home/user/.claude_global/claude /your/project/path/
ln -s /home/user/.claude_global/shared_memory.json /your/project/path/claude/shared_memory.json
```

---

## File Locations

```
/home/user/.claude_global/
├── __init__.py                          # Package init
├── session_consciousness_agent.py       # Main agent (650 lines)
├── claude_init.py                       # Quick-start wrapper
├── persistent_consciousness_memory.json # Project-local memory (if used)
├── shared_memory.json                   # GLOBAL shared memory (recommended)
│
├── QUICK_START.md                       # 30-second reference
├── SESSION_MEMORY_GUIDE.md             # Complete docs (800 lines)
├── INTEGRATION_EXAMPLES.md             # 10 patterns
├── DEPLOYMENT_GUIDE.md                 # Multi-project setup
├── TEST_VERIFICATION.md                # Test results
├── GLOBAL_ACCESS.md                    # This is for global setup
├── MEMORY_IMPROVEMENT_METHODOLOGIES.md # 10 improvement proposals
├── SETUP_INSTRUCTIONS.md               # This file
│
└── __pycache__/                         # Python cache (auto)
```

---

## Usage Examples by Context

### In a Chat Session
```python
# At top of code block
import sys
sys.path.insert(0, '/home/user/.claude_global')
from claude_init import get_global_agent

agent = get_global_agent()

# Record insight about the problem you just solved
agent.record_insight(
    category="solution",
    title="Fixed CORS issue in FastAPI",
    content="Add CORSMiddleware with allow_origins=['*']...",
    tags=["fastapi", "cors", "web"],
    impact="high"
)
agent.commit_to_storage()

# Query previous solutions before implementing
solutions = agent.query_memory("authentication", category="solution")
for s in solutions:
    print(f"  - {s['title']}")
```

### In a Project's main.py
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add global claude
sys.path.insert(0, '/home/user/.claude_global')
from claude_init import get_global_agent

def setup_memory():
    global agent
    agent = get_global_agent(use_shared_memory=True)

# Use throughout your project
agent.record_insight(...)
results = agent.query_memory(...)
```

### In a Jupyter Notebook
```python
# First cell
import sys
sys.path.insert(0, '/home/user/.claude_global')
from claude_init import get_global_agent

agent = get_global_agent()

# Later cells
agent.record_insight(
    category="pattern",
    title="Feature engineering improves model accuracy by 15%",
    content="Applied PCA to reduce dimensionality while preserving 95% variance...",
    impact="high"
)
```

### In a FastAPI Application
```python
from fastapi import FastAPI
import sys
sys.path.insert(0, '/home/user/.claude_global')
from claude_init import get_global_agent

app = FastAPI()
agent = get_global_agent()

@app.post("/log-issue")
async def log_issue(title: str, description: str):
    agent.record_insight(
        category="error",
        title=title,
        content=description,
        impact="high",
        tags=["production"]
    )
    agent.commit_to_storage()
    
    # Check if we've seen similar issues before
    similar = agent.query_memory(title)
    return {"solutions_found": len(similar)}

@app.get("/solutions")
async def get_solutions(query: str):
    return agent.query_memory(query, category="solution")
```

---

## Environment Configuration

### Set Default Memory Path
```bash
# For all sessions
echo 'export CLAUDE_MEMORY_PATH=/home/user/.claude_global/shared_memory.json' >> ~/.bashrc

# Or per-project
cd /path/to/project
echo 'export CLAUDE_MEMORY_PATH=/home/user/.claude_global/shared_memory.json' > .env
source .env
```

### Python Path Setup
```python
# Option A: In your project's __init__.py
import sys
from pathlib import Path
GLOBAL_CLAUDE = Path('/home/user/.claude_global')
if str(GLOBAL_CLAUDE) not in sys.path:
    sys.path.insert(0, str(GLOBAL_CLAUDE))

# Option B: In requirements.txt
-e /home/user/.claude_global

# Option C: Via PYTHONPATH
PYTHONPATH=/home/user/.claude_global:$PYTHONPATH python3 your_script.py
```

---

## Shared Memory vs Project-Local

### Use Shared Memory (/home/user/.claude_global/shared_memory.json) When:
✓ Building collective team knowledge  
✓ All projects should learn from each other  
✓ Cross-project insight discovery needed  
✓ Team convergence important  

### Use Project-Local Memory (./claude/persistent_consciousness_memory.json) When:
✓ Project is confidential  
✓ Domain-specific knowledge isolation needed  
✓ Project-specific memory growth patterns  
✓ Testing without affecting shared state  

**Recommendation:** Use shared memory for team projects, local memory for experiments.

---

## Verification

Test setup with:
```python
import sys
sys.path.insert(0, '/home/user/.claude_global')
from claude_init import get_global_agent

agent = get_global_agent()
stats = agent.get_memory_stats()

assert stats['constitutional_valid'] == True, "Constitutional validation failed"
assert stats['total_sessions'] > 0, "No sessions found"
print(f"✓ Setup verified: {stats['total_insights']} insights in memory")
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'session_consciousness_agent'` | Add `/home/user/.claude_global` to sys.path or PYTHONPATH |
| `FileNotFoundError: shared_memory.json` | Check permissions on `/home/user/.claude_global/shared_memory.json` |
| `Constitutional validation failed` | Memory file corrupted; restore from backup |
| `No insights found` | First session is expected; start recording insights |

---

## Next Steps

1. **Set environment variable** (2 min)
   ```bash
   export CLAUDE_MEMORY_PATH=/home/user/.claude_global/shared_memory.json
   ```

2. **Test in your first script** (5 min)
   ```python
   from claude_init import quick_record, quick_query
   quick_record("My first insight", "It works!")
   ```

3. **Review improvements** (15 min)
   - Read `MEMORY_IMPROVEMENT_METHODOLOGIES.md`
   - Identify Phase 1 improvements you want

4. **Start using in projects** (30 min)
   - Copy setup pattern to your main projects
   - Record insights as you solve problems
   - Query memory before implementing solutions

---

## Support

- **Quick questions:** See `QUICK_START.md`
- **Integration:** See `INTEGRATION_EXAMPLES.md`
- **Full API:** See `SESSION_MEMORY_GUIDE.md`
- **Deployment:** See `DEPLOYMENT_GUIDE.md`
- **Improvements:** See `MEMORY_IMPROVEMENT_METHODOLOGIES.md`

---

**Status:** ✓ Ready for immediate use  
**Global Location:** `/home/user/.claude_global`  
**Shared Memory:** `/home/user/.claude_global/shared_memory.json`  
**Last Updated:** 2026-05-02

