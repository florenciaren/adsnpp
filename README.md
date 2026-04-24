# ADSNPP — Algorithmic Decision System for Nuclear Power Plants

[![CI](https://github.com/florenciaren/adsnpp/actions/workflows/ci.yml/badge.svg)](https://github.com/florenciaren/adsnpp/actions)
[![codecov](https://codecov.io/gh/florenciaren/adsnpp/branch/main/graph/badge.svg)](https://codecov.io/gh/florenciaren/adsnpp)
[![License: EUPL-1.2](https://img.shields.io/badge/License-EUPL_1.2-blue.svg)](https://eupl.eu/1.2/en/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![IAEA ONCORE-26](https://img.shields.io/badge/IAEA%20ONCORE--26-Lausanne%202026-orange)](https://conferences.iaea.org/event/458/)
[![OpenAPI](https://img.shields.io/badge/API-OpenAPI%203.1-green)](https://adsnpp.readthedocs.io/api)

> **Open-source platform for evidence-based nuclear reactor selection integrating parallel Monte Carlo uncertainty quantification, AI/ML risk classification, blockchain governance, and circular economy frameworks for newcomer nuclear countries.**

---

## 🔬 About

ADSNPP was developed to address a critical gap in nuclear energy governance: the absence of transparent, reproducible, and internationally auditable tools for reactor technology selection in newcomer countries pursuing nuclear power for the first time.

The platform is presented at the **IAEA Second Technical Meeting on Open-Source Software for Nuclear Engineering (ONCORE-26)**, EPFL Lausanne, July 20–24, 2026 — Topic T3: *Recent Developments of OSS and Collaborative Initiatives* (parallel simulations, GPU acceleration, new numerical methods).

**Author:** Dr. Florencia Renteria del Toro, PhD  
IAEA Fellow | UNENE Instructor | WiN Global | NAYGN Mexico Region Lead

---

## ✨ Key Features

| Module | Description | Standards |
|--------|-------------|-----------|
| **AHP/TOPSIS Engine** | 47-indicator MCDA across 6 criterion clusters | IAEA NG-G-3.1, INPRO |
| **Parallel Monte Carlo** | 10,000-sample Bayesian uncertainty quantification (CPU/GPU) | ISO/IEC 23053 |
| **XGBoost Classifier** | Procurement outcome risk prediction (340+ historical cases) | IEEE 7001 |
| **BERT NLP Scanner** | Automated regulatory compliance gap detection | IAEA IRRS/INIR |
| **N-CEF Scorer** | 5-dimension nuclear circular economy index | N-CEF v2, ISO 14040 |
| **Blockchain Layer** | Hyperledger Fabric — nuclear material passports + CE credits | INFCIRC/153, ISO/TC 307 |
| **DIRI Assessment** | Digital Infrastructure Readiness Index for newcomer countries | ITU, IAEA NSS-17 |
| **FastAPI Gateway** | REST + GraphQL API, JWT auth, OpenAPI 3.1 docs | W3C WCAG 2.1 |

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+  |  Node.js 20+  |  Go 1.21+  |  Docker + Compose
```

### Installation

```bash
git clone https://github.com/florenciaren/adsnpp.git
cd adsnpp
pip install -r requirements.txt
```

### Run the API server

```bash
uvicorn adsnpp.api.gateway:create_app --factory --host 0.0.0.0 --port 8000 --reload
# → Docs at http://localhost:8000/api/docs
```

### Run MCDA evaluation (Python)

```python
from adsnpp.circular.ncef_engine import NCEFScoringEngine

ce = NCEFScoringEngine()
results = ce.compare_technologies({
    "BWRX-300": {
        "uranium_utilization_efficiency": 0.79,
        "outlet_temp_celsius": 285,
        "hlw_volume_norm": 0.30,
        "hydrogen_production_readiness": 0.20,
        "grid_expansion_potential": 0.85,
        "thermal_efficiency": 0.34,
        "local_content_fraction": 0.45,
        "digital_twin_maturity": 0.82,
        "coolant_recycle_fraction": 0.92,
    },
    "HTR-PM": {
        "uranium_utilization_efficiency": 0.82,
        "outlet_temp_celsius": 750,
        "hlw_volume_norm": 0.25,
        "hydrogen_production_readiness": 0.78,
        "grid_expansion_potential": 0.72,
        "thermal_efficiency": 0.42,
        "local_content_fraction": 0.35,
        "digital_twin_maturity": 0.71,
        "coolant_recycle_fraction": 0.88,
    },
})
for r in results:
    print(f"{r.technology}: CEI = {r.adjusted_cei:.4f}")
# → HTR-PM: CEI = 0.8213
# → BWRX-300: CEI = 0.8071
```

### Docker Compose (all services)

```bash
docker-compose up -d
# Services: api (8000), dashboard (3000), blockchain-node (7051), prometheus (9090)
```

---

## 🏗️ Repository Structure

```
adsnpp/
├── core/               # AHP/TOPSIS/Bayesian decision engine
├── ai/                 # XGBoost, BERT, Federated Learning
├── circular/           # N-CEF scoring, LCA, Material Passports
├── blockchain/         # Hyperledger Fabric chaincode (Go) + Python SDK
├── diri/               # Digital Infrastructure Readiness Index
├── api/                # FastAPI gateway (REST + GraphQL)
├── viz/                # React + D3.js dashboard
├── infra/              # Terraform, Kubernetes, Docker
├── tests/              # Unit, integration, security
└── docs/               # MkDocs documentation site
```

---

## 📊 Parallel Performance

| Environment | N=10,000 samples | Speedup vs Sequential |
|-------------|----------------|-----------------------|
| Sequential (1 core) | 47.3 s | 1× |
| 4-core CPU | 13.1 s | 3.6× |
| 16-core CPU | 3.4 s | 13.8× |
| NVIDIA A100 GPU (CuPy) | 0.9 s | 52.6× |

---

## 🔗 Integration Touchpoints

- **[IAEA PRIS](https://pris.iaea.org)** — Live reactor performance data
- **[OpenMC](https://openmc.org)** — Neutronics validation of fuel utilization scores
- **[RAVEN (INL)](https://raven.inl.gov)** — Uncertainty quantification interoperability
- **[Brightway2](https://brightway.dev)** / [ecoinvent 3.9](https://ecoinvent.org) — LCA inventory
- **[Hyperledger Fabric](https://hyperledger.org/use/fabric)** — Blockchain ledger
- **IAEA InTouch+** — Safeguards reporting integration (planned)

---

## 📋 Standards Compliance

| Domain | Standards |
|--------|-----------|
| Nuclear Safety | IAEA SSR-2/1, GS-R-3, NG-G-3.1 |
| Safeguards | IAEA INFCIRC/153, NSS-17 |
| LCA | ISO 14040/14044 |
| Cybersecurity | IEC 62645, IAEA NSS-17 |
| AI/ML | IEEE 7001, ISO/IEC 23053 |
| Blockchain | ISO/TC 307, Hyperledger Fabric v2.5 |
| API | OpenAPI 3.1, W3C WCAG 2.1 |

---

## 🤝 Contributing

Contributions are warmly welcomed from the ONCORE community!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add neutronics connector'`
4. Push and open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and ensure all tests pass (`pytest tests/`).

**Priority contribution areas:**
- OpenMC / SERPENT2 fuel utilization data connectors
- APROS thermal-hydraulic co-simulation bridge
- Additional reactor technology profiles
- Translation of documentation (Spanish, Arabic, French — IAEA working languages)

---

## 📄 License

This project is licensed under the **European Union Public Licence v1.2 (EUPL-1.2)**.  
See [LICENSE](LICENSE) for full terms.

---

## 📚 Citation

If you use ADSNPP in your research, please cite:

```bibtex
@inproceedings{renteria2026adsnpp,
  author    = {Renteria del Toro, Florencia},
  title     = {{ADSNPP}: An Open-Source Algorithmic Decision Platform for Nuclear
               Reactor Selection Using Parallel {Monte Carlo}, {AI/ML} Methods
               and Blockchain Governance},
  booktitle = {Proceedings of the IAEA Second Technical Meeting on Development
               and Application of Open-Source Software for Nuclear Engineering
               (ONCORE-26)},
  address   = {EPFL Lausanne, Switzerland},
  month     = {July},
  year      = {2026},
  url       = {https://github.com/florenciaren/adsnpp}
}
```

---

## 📬 Contact

**Dr. Florencia Renteria del Toro, PhD**  
GitHub: [@florenciaren](https://github.com/florenciaren)  
IAEA Event 458 | ONCORE-26 | Lausanne, Switzerland | July 2026
