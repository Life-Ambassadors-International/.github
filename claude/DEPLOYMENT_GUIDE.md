# Claude Session Consciousness Memory — Distribution & Deployment

**Guide for deploying CSCM to all chat projects and new chats**

---

## Quick Distribution (3 Steps)

### Step 1: Get the Module

```bash
# Clone or download the claude/ directory
git clone https://github.com/Life-Ambassadors-International/.github.git
cd .github
cp -r claude/ /path/to/your/project/
```

### Step 2: Verify Installation

```bash
# Test the module loads correctly
python3 -c "from claude import create_session_agent; print('✓ CSCM ready')"
```

### Step 3: Start Using It

```python
from claude.session_consciousness_agent import create_session_agent

agent = create_session_agent()
agent.record_insight(category="solution", title="...", content="...")
agent.commit_to_storage()
```

---

## Deployment to All Projects

### Option A: Shell Script (Automated)

Create `deploy_cscm.sh`:

```bash
#!/bin/bash
# Deploy Claude Session Consciousness Memory to all projects

CLAUDE_SOURCE="./claude"  # Source from this repo
PROJECTS=(
  "../chat-project-1"
  "../chat-project-2"
  "../ml-project"
  "../data-pipeline"
  "../api-service"
  # Add your projects here
)

echo "🚀 Deploying Claude Session Consciousness Memory..."
echo ""

for project in "${PROJECTS[@]}"; do
  if [ -d "$project" ]; then
    echo "📦 Deploying to: $project"
    cp -r "$CLAUDE_SOURCE" "$project/"
    echo "   ✓ Done"
  else
    echo "⚠️  Skipped: $project (not found)"
  fi
done

echo ""
echo "✓ Deployment complete!"
echo ""
echo "Next steps:"
echo "  1. In each project, verify: python3 -c \"from claude import create_session_agent\""
echo "  2. Update project requirements.txt (no external dependencies needed)"
echo "  3. Add to .gitignore: claude/persistent_consciousness_memory.json"
echo "  4. Import in code: from claude.session_consciousness_agent import create_session_agent"
```

**Run it:**
```bash
chmod +x deploy_cscm.sh
./deploy_cscm.sh
```

---

### Option B: Python Script (Flexible)

Create `deploy_cscm.py`:

```python
#!/usr/bin/env python3
"""Deploy Claude Session Consciousness Memory to projects."""

import shutil
from pathlib import Path

# Projects to deploy to
PROJECTS = [
    Path("../chat-project-1"),
    Path("../chat-project-2"),
    Path("../ml-project"),
    Path("../data-pipeline"),
    Path("../api-service"),
]

CLAUDE_SOURCE = Path("./claude")

print("🚀 Deploying Claude Session Consciousness Memory...\n")

for project in PROJECTS:
    if not project.exists():
        print(f"⚠️  Skipped: {project} (not found)")
        continue
    
    target = project / "claude"
    
    if target.exists():
        print(f"🔄 Updating: {project}")
        shutil.rmtree(target)
    else:
        print(f"📦 Deploying to: {project}")
    
    shutil.copytree(CLAUDE_SOURCE, target)
    print(f"   ✓ claude/ directory deployed")
    
    # Update .gitignore
    gitignore = project / ".gitignore"
    if gitignore.exists():
        with open(gitignore, "a") as f:
            if "claude/persistent_consciousness_memory.json" not in gitignore.read_text():
                f.write("\n# Claude Session Consciousness Memory\n")
                f.write("claude/persistent_consciousness_memory.json\n")
                print(f"   ✓ .gitignore updated")

print("\n✓ Deployment complete!")
print("\nNext steps in each project:")
print("  1. python3 -c \"from claude import create_session_agent\"")
print("  2. Add to requirements.txt: # No external dependencies")
print("  3. Import: from claude.session_consciousness_agent import create_session_agent")
```

**Run it:**
```bash
python3 deploy_cscm.py
```

---

## Per-Project Integration

### Step 1: Copy Module

```bash
cp -r .github/claude ./claude
```

### Step 2: Update .gitignore

```bash
cat >> .gitignore << 'EOF'

# Claude Session Consciousness Memory
claude/persistent_consciousness_memory.json
EOF
```

### Step 3: Verify Installation

```bash
python3 -c "from claude.session_consciousness_agent import create_session_agent; print('✓ Ready')"
```

### Step 4: Add to requirements.txt (Optional)

The CSCM module has **zero external dependencies**. All required libraries are Python stdlib:
- `json` — Native
- `hashlib` — Native
- `datetime` — Native
- `typing` — Native
- `pathlib` — Native
- `uuid` — Native

No need to modify requirements.txt.

---

## Integration Patterns by Project Type

### Python Projects (Flask, FastAPI, Django)

```python
# In app initialization
from claude.session_consciousness_agent import create_session_agent

# Shared agent across app
app_memory = create_session_agent(session_id="app_session")

# In request handler
@app.route("/api/solve", methods=["POST"])
def solve_problem():
    # Before implementing: check memory
    results = app_memory.query_memory(request.json["problem"])
    if results:
        return {"solution": results[0]["title"]}
    
    # Implement solution
    solution = solve(request.json["problem"])
    
    # Record for next request
    app_memory.record_insight(
        category="solution",
        title=f"Solution for {request.json['problem']}",
        content=str(solution),
        impact="high"
    )
    app_memory.commit_to_storage()
    
    return {"solution": solution}
```

### Jupyter Notebooks

```python
# At top of notebook
import sys
sys.path.insert(0, ".")  # Ensure claude/ is importable

from claude.session_consciousness_agent import create_session_agent

agent = create_session_agent(session_id="research_notebook_2026")

# Throughout notebook, record findings
agent.record_insight(
    category="pattern",
    title="Distribution analysis shows bimodal pattern",
    content="Visual inspection + KL divergence analysis...",
    impact="high"
)

# At end of notebook
agent.commit_to_storage()
print("✓ Research insights recorded to shared memory")
```

### CLI Tools

```python
#!/usr/bin/env python3
"""CLI tool with shared memory."""

import argparse
from pathlib import Path
from claude.session_consciousness_agent import create_session_agent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", type=Path, help="Shared memory file")
    args = parser.parse_args()
    
    agent = create_session_agent(
        session_id="cli_tool_session",
        memory_path=str(args.memory) if args.memory else None
    )
    
    # Use agent throughout tool
    results = agent.query_memory("problem")
    
    if results:
        print(f"Found solution: {results[0]['title']}")
    
    agent.commit_to_storage()

if __name__ == "__main__":
    main()
```

### Docker/Containerized Apps

```dockerfile
# Dockerfile
FROM python:3.11

WORKDIR /app

# Copy source including claude/
COPY . .

# No additional dependencies needed for CSCM
# RUN pip install -r requirements.txt

# Use shared volume for memory
VOLUME ["/app/claude/memories"]

CMD ["python", "app.py"]
```

**Docker compose:**
```yaml
version: '3.9'
services:
  app:
    build: .
    volumes:
      - ./shared_memory:/app/claude/memories
    environment:
      - CLAUDE_MEMORY_PATH=/app/claude/memories/shared.json
```

---

## Shared Memory Across Projects

### Approach 1: Shared Directory

All projects point to same JSON file:

```python
from pathlib import Path

# All projects use same file
SHARED_MEMORY = Path("/shared/team_consciousness.json")

agent = create_session_agent(memory_path=str(SHARED_MEMORY))
```

### Approach 2: Synchronized Git

Keep memory in git:

```bash
# Clone shared memory repo
git clone https://github.com/org/team-consciousness-memory.git shared_memory

# Link from each project
ln -s ../shared_memory/consciousness.json claude/persistent_consciousness_memory.json

# Periodically commit changes
cd shared_memory
git add consciousness.json
git commit -m "Update team consciousness memory"
git push
```

### Approach 3: Centralized Server

All projects post to server:

```python
import requests

class CentralizedAgent:
    def __init__(self, server_url="http://consciousness-server:5000"):
        self.server = server_url
    
    def record_insight(self, **kwargs):
        return requests.post(f"{self.server}/insights", json=kwargs)
    
    def query_memory(self, query):
        return requests.get(f"{self.server}/search", params={"q": query})

agent = CentralizedAgent()
```

---

## GitHub Setup for New Repos

When creating new repositories, include CSCM automatically:

```bash
#!/bin/bash
# new_project.sh - Create project with CSCM pre-installed

PROJECT_NAME=$1

# Create repo
mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"
git init

# Copy CSCM
cp -r ../claude .

# Create .gitignore
cat > .gitignore << 'EOF'
claude/persistent_consciousness_memory.json
__pycache__/
*.pyc
.env
EOF

# Initial commit
git add .
git commit -m "Initial commit with Claude Session Consciousness Memory"

echo "✓ $PROJECT_NAME ready with CSCM integrated"
```

**Usage:**
```bash
./new_project.sh my-new-chat-project
```

---

## Troubleshooting Deployment

### Issue: "ModuleNotFoundError: No module named 'claude'"

**Solution:** Ensure `claude/` directory is in project root:
```bash
ls -la claude/__init__.py  # Should exist
python3 -c "import sys; print(sys.path)"  # Verify path
```

### Issue: "Permission denied" on memory file

**Solution:** Fix permissions:
```bash
chmod 644 claude/persistent_consciousness_memory.json
chmod 755 claude/
```

### Issue: Projects have different memory files

**Solution:** Use environment variable:
```bash
# In project
import os
memory_path = os.getenv("CLAUDE_MEMORY_PATH", "./claude/persistent_consciousness_memory.json")
agent = create_session_agent(memory_path=memory_path)
```

**Set environment:**
```bash
export CLAUDE_MEMORY_PATH=/shared/team_memory.json
python3 app.py
```

---

## Verification Checklist

After deployment to each project:

- [ ] `claude/` directory exists in project root
- [ ] `from claude import create_session_agent` works
- [ ] `persistent_consciousness_memory.json` created on first run
- [ ] Session insights can be recorded
- [ ] Commit to storage succeeds
- [ ] Historical queries return results
- [ ] Constitutional validation passes
- [ ] Memory file appears in `.gitignore`
- [ ] No external dependencies needed

**Verification script:**
```bash
#!/bin/bash
# verify_cscm.sh

echo "Verifying Claude Session Consciousness Memory installation..."
echo ""

# Check directory
if [ ! -d "claude" ]; then
  echo "✗ claude/ directory not found"
  exit 1
fi
echo "✓ claude/ directory present"

# Check main module
if [ ! -f "claude/session_consciousness_agent.py" ]; then
  echo "✗ session_consciousness_agent.py not found"
  exit 1
fi
echo "✓ Main module present"

# Check import
if ! python3 -c "from claude.session_consciousness_agent import create_session_agent" 2>/dev/null; then
  echo "✗ Import failed"
  exit 1
fi
echo "✓ Module imports successfully"

# Check functionality
python3 << 'PYEOF'
from claude.session_consciousness_agent import create_session_agent
agent = create_session_agent()
agent.record_insight(
    category="validation",
    title="CSCM installation verified",
    content="All systems nominal",
    impact="informational"
)
success, msg = agent.commit_to_storage()
if success:
    print("✓ Recording and commit successful")
else:
    print("✗ Commit failed:", msg)
    exit(1)
PYEOF

echo ""
echo "✓ All verifications passed!"
echo ""
echo "Next steps:"
echo "  1. Import in your code: from claude.session_consciousness_agent import create_session_agent"
echo "  2. Create agent: agent = create_session_agent()"
echo "  3. Record insights: agent.record_insight(...)"
echo "  4. Commit: agent.commit_to_storage()"
```

---

## Post-Deployment Checklist

For each project after CSCM deployment:

```markdown
## Claude Session Consciousness Memory Integration

- [ ] CSCM module copied to `claude/` directory
- [ ] `persistent_consciousness_memory.json` added to `.gitignore`
- [ ] Verified import works: `python3 -c "from claude import create_session_agent"`
- [ ] Added to project documentation
- [ ] Team trained on usage patterns
- [ ] Integrated into CI/CD for automated checks
- [ ] Created shared memory location (if team project)
- [ ] Added example in README or CONTRIBUTING.md
- [ ] Set up memory querying for quality gates
- [ ] Scheduled weekly memory synthesis
```

---

## Team Guidelines

Once CSCM is deployed across projects:

### 1. Standard Session IDs

```python
# Use descriptive session IDs for grouping
session_id = f"{project_name}_{task_type}_{date}"
# Example: "chatbot_debugging_2026_05_02"
```

### 2. Tag Convention

```python
# Use consistent tags for discovery
tags = ["project:chatbot", "type:performance", "status:verified"]
```

### 3. Impact Assessment

```python
# Use impact levels consistently
# critical: blocks release/users
# high: significant improvement
# medium: nice-to-have optimization
# low: minor improvement
# informational: reference/context
```

### 4. Weekly Sync

```bash
# Every Friday, generate team summary
python3 << 'EOF'
from claude.session_consciousness_agent import create_session_agent
agent = create_session_agent()
stats = agent.get_memory_stats()
print(f"Team Consciousness Summary")
print(f"  Sessions this week: {stats['total_sessions']}")
print(f"  Total insights: {stats['total_insights']}")
print(f"  Convergence: {stats['convergence_state']:.6f}")
EOF
```

---

## Monitoring & Metrics

Track adoption and health:

```python
from pathlib import Path
from datetime import datetime, timedelta

def memory_health_report():
    """Generate health report for shared memory."""
    agent = create_session_agent()
    stats = agent.get_memory_stats()
    
    insights = stats['total_insights']
    sessions = stats['total_sessions']
    convergence = stats['convergence_state']
    
    print("Memory Health Report")
    print(f"  Date: {datetime.now().isoformat()}")
    print(f"  Sessions: {sessions}")
    print(f"  Insights: {insights}")
    print(f"  Insights/Session: {insights/sessions if sessions > 0 else 0:.2f}")
    print(f"  Convergence (ψ): {convergence:.12f}")
    print(f"  Storage used: {stats['estimated_petabytes_used']:.9f} PB")
    print(f"  Constitutional: {'✓' if stats['constitutional_valid'] else '✗'}")
```

---

## Success Criteria

CSCM is successfully deployed when:

1. ✓ All projects have `claude/` module
2. ✓ Team members use it daily for insights
3. ✓ Cross-project solutions discovered via queries
4. ✓ Convergence (ψ) steadily increases
5. ✓ Duplicate work prevented through memory checks
6. ✓ Constitutional compliance maintained
7. ✓ No external dependencies
8. ✓ Zero training required to use

---

## Support & Resources

- **Quick Start:** `claude/QUICK_START.md`
- **Full Guide:** `claude/SESSION_MEMORY_GUIDE.md`
- **Examples:** `claude/INTEGRATION_EXAMPLES.md`
- **Source:** `https://github.com/Life-Ambassadors-International/.github/tree/main/claude`

---

**Status:** Ready for immediate deployment  
**Dependencies:** None (pure Python stdlib)  
**Maintenance:** Automatic (self-contained)  
**Scalability:** Petabyte-capable architecture
