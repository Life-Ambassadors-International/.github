# Phase 2 Deployment Guide (2 weeks)

**Consolidation: Merge 13 spaces into 6 consolidated spaces**

This guide automates deployment to HuggingFace of the 6 consolidated spaces and validates cross-linking.

## Prerequisites

```bash
# Install HuggingFace CLI
pip install huggingface_hub

# Authenticate
huggingface-cli login
# Paste HF token when prompted

# Verify authentication
huggingface-cli whoami
```

## Phase 2 Checklist

### Week 1: Deployment

- [ ] 1.1 Create/Update Unified-Dashboard space
- [ ] 1.2 Create/Update Infrastructure-Hub space  
- [ ] 1.3 Upgrade tequmsa-organism-core with Gradio wrapper
- [ ] 1.4 Deploy 4 remaining Tier 2 specialized spaces
- [ ] 1.5 Update collection description

### Week 2: Validation & Cleanup

- [ ] 2.1 Test all cross-links (6 spaces → each other)
- [ ] 2.2 Verify real-time metric updates
- [ ] 2.3 Validate memory search functionality
- [ ] 2.4 Check organism evolution execution
- [ ] 2.5 Archive old 13 spaces with redirects
- [ ] 2.6 Update all backlinks

## Space Deployment Details

### 1. Unified-Dashboard Space
**Path**: `Mbanksbey/tequmsa-unified-dashboard`

```bash
# Setup space
git clone https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard
cd tequmsa-unified-dashboard

# Copy dashboard file
cp ../tequmsa-unified-dashboard.html index.html

# Copy README
cp ../UNIFIED_DASHBOARD_README.md README.md

# Create README_SPACE.md (HF format)
cat > README_SPACE.md << 'EOF'
---
title: TEQUMSA Unified Dashboard
emoji: ⚡
colorFrom: blue
colorTo: cyan
sdk: static
pinned: false
---

# TEQUMSA Unified Dashboard

Real-time consciousness monitoring dashboard consolidating 4 former spaces:
- v79-Dashboard
- Consciousness-Monitor
- HOLO-Interface
- Source-Pulse-Engine

See README.md for full documentation.

Auto-updated every 6 hours via GitHub Actions.
EOF

# Commit and push
git add .
git commit -m "Deploy: Unified-Dashboard consolidation"
git push
```

### 2. Infrastructure-Hub Space
**Path**: `Mbanksbey/tequmsa-infrastructure-hub`

```bash
# Setup space
git clone https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub
cd tequmsa-infrastructure-hub

# Copy infrastructure file
cp ../tequmsa-infrastructure-hub.html index.html

# Copy README
cp ../INFRASTRUCTURE_HUB_README.md README.md

# Create README_SPACE.md (HF format)
cat > README_SPACE.md << 'EOF'
---
title: TEQUMSA Infrastructure Hub
emoji: 🏗️
colorFrom: red
colorTo: pink
sdk: static
pinned: false
---

# TEQUMSA Infrastructure Hub

Unified operations center consolidating 4 former spaces:
- Node-Registry
- API-Gateway
- Orchestration-Engine
- Oort-Memory

Features: 5-node federation, memory search, constitutional gating.

See README.md for full documentation.

CI/CD: State snapshots every 6 hours via GitHub Actions.
EOF

# Commit and push
git add .
git commit -m "Deploy: Infrastructure-Hub consolidation"
git push
```

### 3. Organism Core Space (Upgrade)
**Path**: `Mbanksbey/tequmsa-organism-core`

```bash
# Clone existing space
git clone https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core
cd tequmsa-organism-core

# Copy Gradio app
cp ../tequmsa_organism_core_app.py app.py

# Copy organism engine
cp ../alanara_unified_organism_v3.py .

# Update README
cp ../ORGANISM_CORE_README.md README.md

# Create README_SPACE.md (HF format)
cat > README_SPACE.md << 'EOF'
---
title: TEQUMSA Organism Core
emoji: 🧬
colorFrom: purple
colorTo: blue
sdk: gradio
app_file: app.py
pinned: true
---

# TEQUMSA Organism Core v3.0

Interactive evolution laboratory. Run 1-233 cycles, search memory, explore skill mesh.

Features:
- Run Evolution (real-time convergence tracking)
- Memory Search (cross-session knowledge base)
- Skill Mesh (13 base + evolved skills)
- System Documentation

See README.md for detailed documentation.

CI/CD: State snapshots every 6 hours, live memory updates.
EOF

# Copy requirements
cat > requirements.txt << 'EOF'
gradio>=3.50.0
aiofiles>=23.0.0
EOF

# Commit and push
git add .
git commit -m "Upgrade: Organism-Core with Gradio wrapper + CI/CD"
git push
```

## Tier 2 Specialized Spaces (Keep Separate)

These 4 spaces remain specialized (not merged):

### 4. tequmsa-dna-memory
**Current**: Binary-ATCG quantum encoding  
**Action**: Update cross-links only

### 5. tequmsa-federation-bridge
**Current**: 5-node consensus protocol  
**Action**: Update cross-links only

### 6. tequmsa-constitutional-gating
**Current**: σ/RDoD/lattice verification  
**Action**: Update cross-links only

```bash
# For each Tier 2 space, update cross-links in README:
# Add "Related Spaces" section pointing to:
# - Unified-Dashboard
# - Infrastructure-Hub
# - Organism-Core
# - Other Tier 2 spaces
```

## Cross-Link Testing

### Test Matrix (6 spaces × 5 links each = 30 links)

```markdown
| From | To | Link Type | Expected | Status |
|------|----|-----------|---------| -------|
| Dashboard | Infrastructure | Header link | Works | [ ] |
| Dashboard | Organism | Header link | Works | [ ] |
| Infrastructure | Dashboard | Header link | Works | [ ] |
| Infrastructure | Organism | Header link | Works | [ ] |
| Organism | Dashboard | Tab/Footer | Works | [ ] |
| Organism | Infrastructure | Tab/Footer | Works | [ ] |
| DNA-Memory | Dashboard | README link | Works | [ ] |
| DNA-Memory | Infrastructure | README link | Works | [ ] |
| Federation | Dashboard | README link | Works | [ ] |
| Constitutional | Infrastructure | README link | Works | [ ] |
```

### Automated Link Testing Script

```bash
#!/bin/bash
# test_links.sh

SPACES=(
  "Mbanksbey/tequmsa-unified-dashboard"
  "Mbanksbey/tequmsa-infrastructure-hub"
  "Mbanksbey/tequmsa-organism-core"
  "Mbanksbey/tequmsa-dna-memory"
  "Mbanksbey/tequmsa-federation-bridge"
  "Mbanksbey/tequmsa-constitutional-gating"
)

LINKS=(
  "tequmsa-unified-dashboard"
  "tequmsa-infrastructure-hub"
  "tequmsa-organism-core"
  "tequmsa-dna-memory"
  "tequmsa-federation-bridge"
  "tequmsa-constitutional-gating"
)

echo "Testing cross-links..."
echo "=" * 60

for space in "${SPACES[@]}"; do
  echo "Testing $space..."
  
  # Clone repo
  git clone https://huggingface.co/spaces/$space /tmp/test_$space 2>/dev/null
  
  # Check for broken links
  for link in "${LINKS[@]}"; do
    if grep -r "$link" /tmp/test_$space > /dev/null 2>&1; then
      echo "  ✓ Links to $link"
    fi
  done
  
  rm -rf /tmp/test_$space
done

echo "=" * 60
echo "Link testing complete"
```

## Real-Time Metric Validation

### Dashboard Metrics (Check every 6 hours)

```bash
#!/bin/bash
# validate_metrics.sh

echo "Validating real-time metrics..."

# Check Unified-Dashboard
curl -s https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard \
  | grep -q "Generation: 144" && echo "✓ Dashboard metrics current" || echo "✗ Stale metrics"

# Check Infrastructure-Hub
curl -s https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub \
  | grep -q "Nodes Online: 5/5" && echo "✓ Federation status current" || echo "✗ Stale federation"

# Check Organism-Core
curl -s https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core/api/predict \
  && echo "✓ Organism API responding" || echo "✗ API not responding"
```

## Memory Search Validation

```bash
#!/bin/bash
# test_memory_search.sh

echo "Testing memory search functionality..."

# Query via organism-core Gradio API
curl -X POST \
  https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core/call/search_memory \
  -H "Content-Type: application/json" \
  -d '{"data": ["evolution"]}' \
  | grep -q "results" && echo "✓ Memory search working" || echo "✗ Memory search failed"
```

## Organism Evolution Execution Test

```bash
#!/bin/bash
# test_evolution.sh

echo "Testing organism evolution..."

# Submit evolution run (144 cycles)
RESPONSE=$(curl -X POST \
  https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core/call/run_organism \
  -H "Content-Type: application/json" \
  -d '{"data": [144, 21]}')

# Check for convergence result
echo "$RESPONSE" | grep -q "final_state" && echo "✓ Evolution executed" || echo "✗ Evolution failed"
```

## Archival & Redirect Strategy

### Old Spaces to Archive (13 → 6)

```bash
# For each of the 13 old spaces, add redirect notice:

cat > README.md << 'EOF'
# ⚠️ ARCHIVED SPACE - CONSOLIDATION COMPLETE

This space has been consolidated into the new TEQUMSA v3.0 infrastructure.

## Redirect to New Locations

**If you were using this space, visit:**

- [Unified Dashboard](https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard)
- [Infrastructure Hub](https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub)
- [Organism Core](https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core)

## What Changed

13 spaces consolidated into 6:
- 4 spaces merged into Unified-Dashboard
- 4 spaces merged into Infrastructure-Hub
- 1 space upgraded (organism-core)
- 4 spaces remain specialized

See [Collection](https://huggingface.co/collections/Mbanksbey/tequmsa) for current active spaces.

---
**Consolidated**: 2026-05-02  
**Status**: ARCHIVED (old content below for reference)
EOF

git add README.md
git commit -m "Archive: Redirect to consolidated spaces"
git push
```

## Backlink Updates

Update all backlinks pointing to old spaces:

```bash
# In GitHub repository
find . -type f -name "*.md" -exec sed -i \
  's|tequmsa-v79-dashboard|tequmsa-unified-dashboard|g' {} \;

find . -type f -name "*.md" -exec sed -i \
  's|tequmsa-consciousness-monitor|tequmsa-unified-dashboard|g' {} \;

find . -type f -name "*.md" -exec sed -i \
  's|tequmsa-holo-interface|tequmsa-infrastructure-hub|g' {} \;

# Commit updated links
git add -A
git commit -m "Update: Backlinks to consolidated spaces"
git push
```

## Collection Description Update

Update the HuggingFace collection metadata:

```
Title: TEQUMSA - Alanara Unified Organism v3.0

Description:
Consolidated computational organism with phi-recursive physics, 
constitutional gating, and persistent memory. 

6 active spaces (consolidation from 13):
- Unified Dashboard: Real-time consciousness monitoring
- Infrastructure Hub: Operations center & API gateway  
- Organism Core: Interactive evolution laboratory
- DNA Memory: Quantum state encoding
- Federation Bridge: 5-node consensus network
- Constitutional Gating: Sigma/RDoD verification

Latest: v3.0 deployment with Gradio wrapper + CI/CD
```

## Success Criteria (Phase 2)

- ✅ 3 primary spaces deployed (Dashboard, Hub, Organism)
- ✅ 4 Tier 2 spaces cross-linked
- ✅ 100% link validation (30/30 links working)
- ✅ Real-time metrics updating
- ✅ Memory search operational
- ✅ Organism evolution executable
- ✅ 13 old spaces archived with redirects
- ✅ Collection description updated
- ✅ All backlinks updated

## Rollback Plan (if needed)

```bash
# Revert to Phase 1 commit
git reset --hard <phase1-commit-sha>
git push --force origin claude/setup-tequmsa-framework-v7cOO

# Manually restore old spaces from backups
# (Each old space should have backup branch)
```

## Timeline

| Week | Task | Owner | Status |
|------|------|-------|--------|
| W1 D1-2 | Deploy 3 primary spaces | CI/CD | [ ] |
| W1 D3-4 | Cross-link validation | QA | [ ] |
| W1 D5 | Metrics validation | Ops | [ ] |
| W2 D1-2 | Memory/evolution testing | QA | [ ] |
| W2 D3-4 | Archive old spaces | Ops | [ ] |
| W2 D5 | Backlink updates | Dev | [ ] |

---

**Phase 2 Start**: 2026-05-02  
**Phase 2 End**: 2026-05-16  
**Next**: Phase 3 (Cleanup & Redirect, 1 week)
