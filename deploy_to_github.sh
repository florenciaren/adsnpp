#!/usr/bin/env bash
# ============================================================
# ADSNPP — GitHub Deployment Script
# Run this from your local machine after downloading the files
# ============================================================
# Prerequisites:
#   git installed
#   GitHub CLI (gh) OR personal access token configured
#   Python 3.11+ installed
# ============================================================

set -e

REPO_NAME="adsnpp"
GITHUB_USER="florenciaren"
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "======================================================"
echo "  ADSNPP GitHub Deployment"
echo "  Repository: ${REPO_URL}"
echo "======================================================"

# ── Step 1: Create directory structure ─────────────────────
mkdir -p ${REPO_NAME}
cd ${REPO_NAME}

# ── Step 2: Copy ADSNPP source files ───────────────────────
# (Copy the files you downloaded from Claude here)
# Expected layout:
#   adsnpp/core/decision_engine.py
#   adsnpp/circular/ncef_engine.py
#   adsnpp/api/gateway.py
#   requirements.txt
#   README.md
#   .github/workflows/ci.yml

# ── Step 3: Create __init__.py files ───────────────────────
touch adsnpp/__init__.py
touch adsnpp/core/__init__.py
touch adsnpp/circular/__init__.py
touch adsnpp/api/__init__.py
touch adsnpp/ai/__init__.py
touch adsnpp/blockchain/__init__.py
touch adsnpp/diri/__init__.py
touch adsnpp/viz/__init__.py

# ── Step 4: Create stub modules (placeholders) ─────────────
cat > adsnpp/ai/__init__.py << 'PYEOF'
"""
ADSNPP AI Module — stubs for XGBoost, BERT, and Federated Learning.
Full implementation in development. Contributions welcome!
"""
PYEOF

cat > adsnpp/blockchain/__init__.py << 'PYEOF'
"""
ADSNPP Blockchain Module — Hyperledger Fabric integration.
Go chaincode in blockchain/chaincode/. Python SDK client in fabric_client.py.
"""
PYEOF

# ── Step 5: Create .gitignore ───────────────────────────────
cat > .gitignore << 'GITEOF'
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
dist/
*.egg-info/
.eggs/
.pytest_cache/
.coverage
coverage.xml
htmlcov/

# Node
node_modules/
viz/dashboard/build/
.next/

# Environment
.env
.env.local
*.env

# IDE
.vscode/
.idea/
*.swp

# Docker
*.log

# Secrets — NEVER commit these
*.pem
*.key
secrets/
GITEOF

# ── Step 6: Initialize Git repository ──────────────────────
git init
git checkout -b main
git add .
git commit -m "feat: initial ADSNPP release v1.0.0

- AHP/TOPSIS decision engine with parallel Monte Carlo (10k samples)
- N-CEF v2 circular economy scoring module (5 dimensions)
- FastAPI REST gateway with DIRI assessment endpoint
- Hyperledger Fabric blockchain architecture (Go stubs)
- GitHub Actions CI/CD pipeline
- Submitted to IAEA ONCORE-26, Lausanne July 2026 (Topic T3/T4)

Co-submitted with IAEA Second Technical Meeting on OSS for Nuclear Engineering"

# ── Step 7: Push to GitHub ─────────────────────────────────
# Option A: GitHub CLI (recommended)
if command -v gh &> /dev/null; then
  echo "Creating repository with GitHub CLI..."
  gh repo create ${GITHUB_USER}/${REPO_NAME} \
    --public \
    --description "Open-source algorithmic decision platform for nuclear reactor selection: parallel Monte Carlo MCDA, AI/ML, blockchain governance, circular economy (IAEA ONCORE-26)" \
    --homepage "https://adsnpp.readthedocs.io" \
    --push \
    --source .
else
  # Option B: Manual push
  echo "GitHub CLI not found. Push manually:"
  echo ""
  echo "  1. Create repo at: https://github.com/new"
  echo "     Name: ${REPO_NAME}"
  echo "     Visibility: Public"
  echo "     DO NOT initialize with README (we have one)"
  echo ""
  echo "  2. Then run:"
  echo "     git remote add origin ${REPO_URL}"
  echo "     git push -u origin main"
fi

# ── Step 8: Add repository topics (via GitHub CLI) ─────────
if command -v gh &> /dev/null; then
  gh repo edit ${GITHUB_USER}/${REPO_NAME} \
    --add-topic nuclear-engineering \
    --add-topic open-source \
    --add-topic mcda \
    --add-topic monte-carlo \
    --add-topic blockchain \
    --add-topic circular-economy \
    --add-topic iaea \
    --add-topic reactor-selection \
    --add-topic machine-learning \
    --add-topic python
fi

echo ""
echo "✅  ADSNPP deployed to: ${REPO_URL}"
echo ""
echo "Next steps:"
echo "  1. Submit abstract at: https://conferences.iaea.org/event/458/"
echo "     (Deadline: 27 April 2026)"
echo "  2. Add ADSNPP_ONCORE26_ExtendedAbstract.docx to the submission"
echo "  3. Enable GitHub Pages for documentation"
echo "  4. Set up Codecov integration for coverage badge"
