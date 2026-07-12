# ADSNPP — Algorithmic Decision System for Nuclear Power Plants

Open-source platform for evidence-based nuclear reactor selection,
integrating parallel Monte Carlo uncertainty quantification, AI/ML risk
classification, blockchain governance, and circular economy frameworks
for newcomer nuclear countries.

Presented at the **IAEA Second Technical Meeting on Open-Source Software
for Nuclear Engineering (ONCORE-26)**, EPFL Lausanne, July 20-24, 2026.

## Live simulation

[Open the ADSNPP ONCORE-26 simulation](simulation.html){ .md-button }

## API reference

Run the FastAPI gateway locally:

```bash
pip install -r requirements.txt
uvicorn adsnpp.api.gateway:create_app --factory --host 0.0.0.0 --port 8000 --reload
```

Interactive docs are then served at `http://localhost:8000/api/docs`.

## Source

See the [GitHub repository](https://github.com/florenciaren/adsnpp) for
source code, tests, and the N-CEF circular economy scoring engine.
