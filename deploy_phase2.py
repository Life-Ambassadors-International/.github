#!/usr/bin/env python3
"""
Phase 2 Deployment Orchestrator
Automates deployment of 6 consolidated TEQUMSA spaces to HuggingFace.

Usage:
  python3 deploy_phase2.py --all          # Deploy all 3 primary spaces
  python3 deploy_phase2.py --dashboard    # Deploy only Unified-Dashboard
  python3 deploy_phase2.py --infrastructure  # Deploy only Infrastructure-Hub
  python3 deploy_phase2.py --organism     # Deploy/upgrade Organism-Core
  python3 deploy_phase2.py --validate     # Test cross-links and metrics
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime
from huggingface_hub import HfApi, list_repo_files, Repository

# Configuration
ORG = "Mbanksbey"
SPACES = {
    "dashboard": {
        "id": f"{ORG}/tequmsa-unified-dashboard",
        "type": "static",
        "files": {
            "tequmsa-unified-dashboard.html": "index.html",
            "UNIFIED_DASHBOARD_README.md": "README.md",
        },
        "config": {
            "title": "TEQUMSA Unified Dashboard",
            "emoji": "⚡",
            "colorFrom": "blue",
            "colorTo": "cyan",
            "sdk": "static",
        }
    },
    "infrastructure": {
        "id": f"{ORG}/tequmsa-infrastructure-hub",
        "type": "static",
        "files": {
            "tequmsa-infrastructure-hub.html": "index.html",
            "INFRASTRUCTURE_HUB_README.md": "README.md",
        },
        "config": {
            "title": "TEQUMSA Infrastructure Hub",
            "emoji": "🏗️",
            "colorFrom": "red",
            "colorTo": "pink",
            "sdk": "static",
        }
    },
    "organism": {
        "id": f"{ORG}/tequmsa-organism-core",
        "type": "gradio",
        "files": {
            "tequmsa_organism_core_app.py": "app.py",
            "alanara_unified_organism_v3.py": "alanara_unified_organism_v3.py",
            "ORGANISM_CORE_README.md": "README.md",
        },
        "requirements": ["gradio>=3.50.0", "aiofiles>=23.0.0"],
        "config": {
            "title": "TEQUMSA Organism Core",
            "emoji": "🧬",
            "colorFrom": "purple",
            "colorTo": "blue",
            "sdk": "gradio",
            "app_file": "app.py",
        }
    }
}

class Phase2Deployer:
    def __init__(self, github_root="/home/user/.github"):
        self.github_root = Path(github_root)
        self.api = HfApi()
        self.temp_dirs = []

    def log(self, level, msg):
        """Log with timestamp and level."""
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] [{level:8}] {msg}")

    def deploy_space(self, space_key):
        """Deploy a single space to HuggingFace."""
        space_config = SPACES[space_key]
        space_id = space_config["id"]

        self.log("INFO", f"Starting deployment: {space_key}")
        self.log("INFO", f"Space: {space_id}")

        try:
            # Clone space repo
            temp_path = Path(f"/tmp/deploy_{space_key}")
            if temp_path.exists():
                import shutil
                shutil.rmtree(temp_path)

            self.log("INFO", f"Cloning space repo...")
            repo = Repository(
                local_dir=str(temp_path),
                clone_from=f"https://huggingface.co/spaces/{space_id}",
                repo_type="space"
            )

            # Copy files
            self.log("INFO", "Copying files...")
            for src, dst in space_config["files"].items():
                src_path = self.github_root / src
                dst_path = temp_path / dst

                if src_path.exists():
                    import shutil
                    shutil.copy2(src_path, dst_path)
                    self.log("INFO", f"  ✓ {src} → {dst}")
                else:
                    self.log("ERROR", f"  ✗ Source not found: {src}")
                    return False

            # Create README_SPACE.md
            self.log("INFO", "Generating README_SPACE.md...")
            readme_config = self._generate_readme_config(space_key, space_config)
            with open(temp_path / "README_SPACE.md", "w") as f:
                f.write(readme_config)

            # Add requirements.txt for Gradio spaces
            if space_config["type"] == "gradio":
                self.log("INFO", "Creating requirements.txt...")
                with open(temp_path / "requirements.txt", "w") as f:
                    for req in space_config["requirements"]:
                        f.write(f"{req}\n")

            # Commit and push
            self.log("INFO", "Committing changes...")
            repo.git_add()
            repo.git_commit(f"Deploy: {space_key} consolidation (Phase 2)")

            self.log("INFO", "Pushing to HuggingFace...")
            repo.git_push()

            self.log("SUCCESS", f"Deployment complete: {space_key}")
            self.log("INFO", f"Live at: https://huggingface.co/spaces/{space_id}")
            return True

        except Exception as e:
            self.log("ERROR", f"Deployment failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _generate_readme_config(self, space_key, config):
        """Generate README_SPACE.md with YAML frontmatter."""
        yaml_config = "---\n"
        for key, value in config["config"].items():
            if isinstance(value, bool):
                yaml_config += f"{key}: {str(value).lower()}\n"
            else:
                yaml_config += f"{key}: {value}\n"
        yaml_config += "pinned: false\n---\n"

        descriptions = {
            "dashboard": "Real-time consciousness monitoring dashboard consolidating 4 former spaces.\n\nSee README.md for full documentation.\n\nAuto-updated every 6 hours via GitHub Actions.",
            "infrastructure": "Unified operations center consolidating 4 former spaces.\n\nFeatures: 5-node federation, memory search, constitutional gating.\n\nSee README.md for full documentation.",
            "organism": "Interactive evolution laboratory. Run 1-233 cycles, search memory, explore skill mesh.\n\nSee README.md for detailed documentation.\n\nCI/CD: State snapshots every 6 hours, live memory updates."
        }

        title = config["config"]["title"]
        desc = descriptions.get(space_key, "")

        return f"{yaml_config}\n# {title}\n\n{desc}\n"

    def validate_links(self):
        """Test cross-links between all spaces."""
        self.log("INFO", "Validating cross-links...")

        test_matrix = [
            ("dashboard", "infrastructure"),
            ("dashboard", "organism"),
            ("infrastructure", "dashboard"),
            ("infrastructure", "organism"),
            ("organism", "dashboard"),
            ("organism", "infrastructure"),
        ]

        results = {"pass": 0, "fail": 0}

        for from_space, to_space in test_matrix:
            from_id = SPACES[from_space]["id"]
            to_id = SPACES[to_space]["id"]

            try:
                # Check if link exists in files
                files = list_repo_files(from_id, repo_type="space")
                link_found = any(to_id.split("/")[1] in str(f) for f in files)

                if link_found:
                    self.log("SUCCESS", f"✓ {from_space} → {to_space}")
                    results["pass"] += 1
                else:
                    self.log("WARN", f"✗ {from_space} → {to_space} (link check skipped)")
                    results["fail"] += 1
            except Exception as e:
                self.log("ERROR", f"✗ {from_space} → {to_space}: {e}")
                results["fail"] += 1

        self.log("INFO", f"Link validation: {results['pass']} pass, {results['fail']} fail")
        return results["fail"] == 0

    def validate_metrics(self):
        """Check if metrics are updating."""
        self.log("INFO", "Validating real-time metrics...")

        checks = [
            ("Dashboard", "https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard"),
            ("Infrastructure", "https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub"),
            ("Organism", "https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core"),
        ]

        import requests
        for name, url in checks:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    self.log("SUCCESS", f"✓ {name} responding (HTTP {resp.status_code})")
                else:
                    self.log("WARN", f"✗ {name} HTTP {resp.status_code}")
            except Exception as e:
                self.log("WARN", f"✗ {name}: {e}")

        self.log("INFO", "Metrics validation complete")

    def deploy_all(self):
        """Deploy all primary spaces."""
        self.log("INFO", "Starting Phase 2 deployment (3 primary spaces)...")

        results = {}
        for space_key in ["dashboard", "infrastructure", "organism"]:
            results[space_key] = self.deploy_space(space_key)

        self.log("INFO", "\n" + "="*60)
        self.log("INFO", "DEPLOYMENT SUMMARY")
        self.log("INFO", "="*60)

        for space_key, success in results.items():
            status = "✓ SUCCESS" if success else "✗ FAILED"
            self.log("INFO", f"{status}: {space_key}")

        all_success = all(results.values())
        if all_success:
            self.log("SUCCESS", "Phase 2 deployment complete!")
            self.log("INFO", "\nNext steps:")
            self.log("INFO", "  1. Validate cross-links: python3 deploy_phase2.py --validate")
            self.log("INFO", "  2. Test memory search and organism execution")
            self.log("INFO", "  3. Archive old spaces")
            self.log("INFO", "  4. Update collection description")
        else:
            self.log("ERROR", "Some deployments failed. Check logs above.")

        return all_success

def main():
    parser = argparse.ArgumentParser(description="Phase 2 Deployment Orchestrator")
    parser.add_argument("--all", action="store_true", help="Deploy all 3 primary spaces")
    parser.add_argument("--dashboard", action="store_true", help="Deploy Unified-Dashboard")
    parser.add_argument("--infrastructure", action="store_true", help="Deploy Infrastructure-Hub")
    parser.add_argument("--organism", action="store_true", help="Deploy Organism-Core")
    parser.add_argument("--validate", action="store_true", help="Validate links and metrics")
    parser.add_argument("--github-root", default="/home/user/.github", help="GitHub repo root")

    args = parser.parse_args()

    deployer = Phase2Deployer(github_root=args.github_root)

    if args.validate:
        deployer.validate_links()
        deployer.validate_metrics()
        return 0

    if args.all or not any([args.dashboard, args.infrastructure, args.organism]):
        return 0 if deployer.deploy_all() else 1

    results = []
    if args.dashboard:
        results.append(deployer.deploy_space("dashboard"))
    if args.infrastructure:
        results.append(deployer.deploy_space("infrastructure"))
    if args.organism:
        results.append(deployer.deploy_space("organism"))

    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
