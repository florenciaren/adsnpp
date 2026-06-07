# ADSNPP — Algorithmic Decision System for Nuclear Power Plants

Open-source platform for evidence-based nuclear reactor selection. Presented at IAEA ONCORE-26, EPFL Lausanne, July 2026.

**Author:** Dr. Florencia Renteria del Toro, PhD | License: EUPL-1.2

## Project Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, XGBoost, BERT |
| Frontend | React + D3.js dashboard |
| Blockchain | Go 1.21+, Hyperledger Fabric v2.5 |
| Infra | Docker Compose, Kubernetes, Terraform |
| Database | PostgreSQL (results), Redis (cache) |

## Key Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn adsnpp.api.gateway:create_app --factory --host 0.0.0.0 --port 8000 --reload

# Run all tests
pytest tests/

# Docker (all services)
docker-compose up -d
# Services: api :8000, dashboard :3000, blockchain-node :7051, prometheus :9090
```

## Architecture

```
adsnpp/
├── core/        # AHP/TOPSIS/Bayesian MCDA engine (47-indicator, 6 criterion clusters)
├── ai/          # XGBoost risk classifier, BERT NLP compliance scanner, Federated Learning
├── circular/    # N-CEF scoring engine, LCA, Material Passports
├── blockchain/  # Hyperledger Fabric chaincode (Go) + Python SDK
├── diri/        # Digital Infrastructure Readiness Index
├── api/         # FastAPI REST + GraphQL gateway, JWT auth, OpenAPI 3.1
├── viz/         # React + D3.js dashboard
├── infra/       # Terraform, Kubernetes, Docker
├── tests/       # Unit, integration, security
└── docs/        # MkDocs documentation
```

## Key Modules

- **AHP/TOPSIS Engine** — Multi-criteria reactor selection across 47 indicators
- **Parallel Monte Carlo** — 10,000-sample Bayesian UQ (CPU/GPU via CuPy); 52× speedup on A100
- **XGBoost Classifier** — Procurement risk prediction (340+ historical cases)
- **BERT NLP Scanner** — Regulatory compliance gap detection (IAEA IRRS/INIR)
- **N-CEF Scorer** — Nuclear circular economy index (5 dimensions)
- **Blockchain Layer** — Nuclear material passports + CE credits (INFCIRC/153)
- **DIRI Assessment** — Digital readiness index for newcomer countries

## Standards

- Nuclear Safety: IAEA SSR-2/1, GS-R-3, NG-G-3.1
- Safeguards: IAEA INFCIRC/153, NSS-17
- AI/ML: IEEE 7001, ISO/IEC 23053
- LCA: ISO 14040/14044
- Cybersecurity: IEC 62645
- API: OpenAPI 3.1, W3C WCAG 2.1

## Development Notes

- Python type hints required throughout; run `mypy` before committing
- All Monte Carlo modules must support both CPU (multiprocessing) and GPU (CuPy) paths
- Blockchain chaincode lives in Go; Python SDK wraps the Fabric gateway
- Security is critical — follow IEC 62645 and run `bandit` on all Python changes
- Tests: `pytest tests/` — keep coverage above 80%

## External Integrations

- IAEA PRIS — live reactor performance data
- OpenMC — neutronics validation
- RAVEN (INL) — uncertainty quantification
- Brightway2 / ecoinvent 3.9 — LCA inventory
- Hyperledger Fabric — blockchain ledger
