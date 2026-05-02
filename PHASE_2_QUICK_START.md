# Phase 2 Quick Start - Deploy to HuggingFace

**5-minute setup and deployment guide**

## Step 1: Authenticate with HuggingFace

```bash
# Install/update HF CLI (new `hf` command)
pip install --upgrade huggingface_hub

# Login with your HuggingFace token
hf auth login

# Follow the prompt:
# - Go to https://huggingface.co/settings/tokens
# - Create a new token (write access needed)
# - Paste token when prompted
```

## Step 2: Deploy All Spaces (Option A - Automated)

```bash
cd /home/user/.github

# Deploy all 3 primary spaces at once
python3 deploy_phase2.py --all

# Monitor output - watch for:
# [SUCCESS] sections indicate each space deployed
# [ERROR] sections indicate issues to fix
```

**Estimated time**: 5-10 minutes per space (15-30 minutes total)

## Step 3: Validate Deployment (Option B - Manual)

If you prefer manual deployment, follow the step-by-step guide in `PHASE_2_DEPLOYMENT_GUIDE.md`.

Or deploy spaces individually:

```bash
# Deploy only Unified-Dashboard
python3 deploy_phase2.py --dashboard

# Deploy only Infrastructure-Hub
python3 deploy_phase2.py --infrastructure

# Deploy only Organism-Core
python3 deploy_phase2.py --organism
```

## Step 4: Verify Everything Works

```bash
# Test cross-links between spaces
python3 deploy_phase2.py --validate

# Manually check:
# 1. Visit: https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard
# 2. Visit: https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub
# 3. Visit: https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core
#    - Run the Gradio interface
#    - Try "Run Evolution" with 144 cycles
#    - Try "Memory Search" with "evolution"
```

## Expected Outcomes

### Unified-Dashboard Space
- ✅ Static HTML dashboard loads
- ✅ Shows real-time metrics (generation, skills, federation nodes)
- ✅ Links to Infrastructure-Hub and Organism-Core
- ✅ Updates every 6 hours (via CI/CD snapshots)

### Infrastructure-Hub Space
- ✅ Static HTML operations center loads
- ✅ Shows 5 federation nodes (all online)
- ✅ Shows 5 API endpoints
- ✅ Shows Oort Memory stats (157+ entries)
- ✅ Links to Dashboard and Organism-Core

### Organism-Core Space
- ✅ Gradio interface loads
- ✅ "⚡ Run Evolution" tab works (execute 144 cycles)
- ✅ "🔍 Memory Search" tab works (search with keywords)
- ✅ "🎯 Skill Mesh" tab shows 24 skills
- ✅ "ℹ️ About" tab loads documentation
- ✅ JSON state export works

## Troubleshooting

### "No HF token configured"
```bash
# Run login again
hf auth login

# Or set token via environment
export HF_TOKEN="hf_xxxxxxxxxxxxx"
```

### "Space doesn't exist" error
This is expected on first deployment - the space will be created automatically by the HF CLI.

### Gradio space doesn't start
```bash
# Check requirements.txt exists in space
# Contains: gradio>=3.50.0, aiofiles>=23.0.0

# Check app.py exists and is executable
# Should be: tequmsa_organism_core_app.py
```

### Cross-links don't work
Manually add links to README files:
- Dashboard README: Link to Infrastructure-Hub and Organism-Core  
- Infrastructure README: Link to Dashboard and Organism-Core
- Organism README: Link to Dashboard and Infrastructure

## After Deployment

### Week 1 Follow-up
- [ ] Verify all 3 spaces live and accessible
- [ ] Test cross-links (click links between spaces)
- [ ] Test organism evolution (run 144 cycles)
- [ ] Test memory search (search "evolution")

### Week 2 Follow-up
- [ ] Archive old 13 spaces (add redirect notices)
- [ ] Update collection description
- [ ] Update all backlinks in GitHub repo

## Commands Reference

```bash
# Full deployment
python3 deploy_phase2.py --all

# Deploy single space
python3 deploy_phase2.py --dashboard
python3 deploy_phase2.py --infrastructure
python3 deploy_phase2.py --organism

# Validate deployment
python3 deploy_phase2.py --validate

# Manual space deployment (from CLI)
hf repo create "tequmsa-unified-dashboard" --type space --space-sdk static
git clone https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard
cd tequmsa-unified-dashboard
cp ../tequmsa-unified-dashboard.html index.html
cp ../UNIFIED_DASHBOARD_README.md README.md
git add .
git commit -m "Deploy: Unified-Dashboard"
git push

# HF CLI commands
hf auth login                    # Authenticate
hf auth logout                   # Logout
hf whoami                        # Check current user
hf repos ls --type space         # List your spaces
hf upload path/to/files org/repo # Upload files
```

---

**Status**: Ready for Phase 2 Deployment  
**Time to Deploy**: ~15-30 minutes  
**Dependencies**: HF token (write access), Python 3.8+, huggingface_hub
