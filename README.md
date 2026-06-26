# TrustTraj — Calibrated Abstention in Multi-Step LLM Agents

**Thesis title:** "Calibrated Abstention in Multi-Step LLM Agents: A Trajectory-Aware Reliability Layer for Text-to-SQL Analytics"
**Author:** Sonia Raju | **Institution:** SRH University

## Description

TrustTraj builds a trajectory-aware abstention layer for text-to-SQL LLM agents. Rather than always returning an answer, the system learns *when to say "I don't know"* — improving reliability by abstaining on questions it is likely to get wrong. Four abstention mechanisms (M1–M4) are designed, implemented, and evaluated on the BIRD-mini-dev and TrustSQL benchmarks using two open-weight models (Llama-3.1-8B-Instruct and Qwen-2.5-Coder-7B). The core design principle is *record-once-score-offline*: agent trajectories are generated once on cloud GPUs (Google Colab Pro), cached to disk, then scored locally across all four mechanisms — ensuring fair comparison and reproducibility without re-running expensive inference.

## Repository structure

```
TrustTraj/
├── src/              # Python source code (agent, mechanisms, evaluation)
├── data/             # Datasets — gitignored, download separately
├── trajectories/     # Cached agent trajectories — gitignored, synced from Colab
├── results/          # Metrics, plots, tables (checked in)
├── notebooks/        # Google Colab notebooks for trajectory generation
├── prompts/          # Agent prompt templates (plain text / Jinja2)
├── thesis/           # Thesis chapter drafts (.tex or .docx)
├── docs/             # Reference papers, proposal, notes
├── skills/           # Project-specific instructions for Claude Code
├── logs/             # steplog.md — append-only action log
├── CLAUDE.md         # Instructions for Claude Code (read this first)
├── PROGRESS.md       # Current state and next step (read at every session start)
├── DECISIONS.md      # Decision record (newest first)
├── PREREGISTRATION.md# Pre-registered methodology (frozen at Week 6)
├── plan.md           # 16-week master plan
└── todo.md           # Current checklist
```

## Setup

> Dependencies will be pinned in requirements.txt during Step 3 (Python environment setup).

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Reproduce

Full reproduction instructions will be added after the experiment phase (Phase 3). Key steps will include:
1. Download datasets (BIRD-mini-dev, TrustSQL) per `docs/data_download.md` (TBD).
2. Run trajectory generation notebooks in `notebooks/` on Google Colab Pro.
3. Sync trajectories to `trajectories/`.
4. Run evaluation scripts in `src/` locally.

## License

TBD — to be decided before public release (likely MIT for code, CC BY 4.0 for thesis content).

## Author

Sonia Raju — Master's student, SRH University.
