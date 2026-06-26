# TrustTraj

**Calibrated Abstention in Multi-Step LLM Agents: A Trajectory-Aware Reliability Layer for Text-to-SQL Analytics**

Master's thesis — Sonia Raju, SRH University

---

## What this is

Text-to-SQL agents often return wrong answers confidently. TrustTraj adds a reliability layer that decides *when to answer and when to abstain* — "I don't know" is a valid and sometimes correct response.

The system records the full step-by-step trajectory an LLM agent takes to produce a SQL query, then scores each trajectory using four abstention mechanisms (M1–M4). The key design choice is **record-once, score-offline**: trajectories are generated once on cloud GPUs, cached to disk, and all four mechanisms are evaluated post-hoc on the same trajectories. This guarantees a fair comparison and makes results reproducible without re-running expensive model inference.

---

## Abstention mechanisms

| ID | Name | What it uses |
|----|------|--------------|
| M1 | End-only log-probability threshold | Token log-prob of the final answer step only |
| M2 | Self-consistency (k=5) | Agreement rate across 5 sampled trajectories |
| M3 | Conformal abstention | Distribution-free coverage guarantee at α = 0.10 |
| M4 | Trajectory-feature calibrator | L1-regularised logistic regression on ~12–20 trajectory features (cross-step dynamics, intra-step stability, positional, structural) |

---

## Benchmarks

- **BIRD-mini-dev** — 500 questions across 11 databases; 3 difficulty tiers. A pre-registered stratified sample of 300 (100 per tier, seed 42) is used for primary evaluation.
- **TrustSQL** — 2,830 pairs (feasible + infeasible) from ATIS, Advising, and EHRSQL. Used to evaluate reliability under a penalty-weighted scoring scheme.

---

## Models

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen2.5-Coder-7B-Instruct`

Trajectory generation runs on **Google Colab Pro** (cloud GPU). All evaluation, calibration, and plotting runs locally on a standard laptop.

---

## Repository layout

```
TrustTraj/
├── src/               # Python source — agent, mechanisms, evaluation scripts
├── notebooks/         # Colab notebooks for trajectory generation
├── prompts/           # Agent prompt templates
├── results/           # Metrics, plots, and tables (version-controlled)
├── logs/              # steplog.md — append-only action log
├── data/              # Datasets (gitignored — download separately)
├── trajectories/      # Cached trajectories (gitignored — synced from Colab)
├── PROGRESS.md        # Current state and next step
├── DECISIONS.md       # Decision log (newest first)
├── PREREGISTRATION.md # Pre-registered methodology (frozen at Week 6)
├── plan.md            # 16-week project plan
└── todo.md            # Current task checklist
```

---

## Setup

Python 3.11 is required. From the project root:

```bash
# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

The virtual environment lives at `.venv/` inside the project folder and is not version-controlled.

---

## Reproducing results

Full reproduction instructions will be added after the experiment phase. The high-level steps are:

1. Download BIRD-mini-dev and TrustSQL into `data/` (instructions TBD in `docs/data_download.md`).
2. Run trajectory generation notebooks in `notebooks/` on Google Colab Pro.
3. Sync the output to `trajectories/`.
4. Run evaluation scripts in `src/` locally to produce metrics and plots in `results/`.

All random seeds are fixed at {0, 1, 2} and recorded. All LLM outputs are cached so nothing is recomputed on re-runs.

---

## Pre-registration

The full methodology — research questions, hypotheses, models, benchmarks, abstention mechanisms, evaluation metrics, and statistical analysis plan — is pre-registered in [`PREREGISTRATION.md`](PREREGISTRATION.md) and freezes at Week 6. Any deviation after the freeze is documented there and in [`DECISIONS.md`](DECISIONS.md).

---

## License

To be decided before public release — likely MIT for code, CC BY 4.0 for thesis content.
