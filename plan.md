# plan.md — Master Plan (16 weeks)

## Phase 0 — Foundation (Weeks 1-2)
Repo + governance (Step 1, done). Lock pre-registration. Python environment. GitHub/Zenodo accounts. Literature consolidated into notes.

## Phase 1 — Prototype + data (Weeks 3-4)
Build the text-to-SQL agent (planner -> SQL generator -> executor/verifier) on LangGraph with full trajectory logging. Download and validate BIRD-mini-dev, TrustSQL, Spider. Register a 200-300 question BIRD subset (record selection before any run). Smoke-test the pipeline locally on a tiny 0.5B model.

## Phase 2 — Abstention mechanisms (Weeks 5-6)
Implement M1 (end-only log-prob threshold), M2 (self-consistency, k=5), M3 (conformal abstention with self-evaluation), M4 (trajectory-feature logistic calibrator, ~12-20 L1-regularised features). Feature extraction + unit tests. SCOPE FREEZE at end of Week 6.

## Phase 3 — Experiments on Colab (Weeks 7-9)
Pilot first (1 model, 1 seed, ~50 questions) to measure time and cost. Then full matrix: Llama-3.1-8B-Instruct and Qwen-2.5-Coder-7B across seeds {0,1,2} on the BIRD subset + full TrustSQL (2,830 pairs); optional GPT-4o-mini on 100 items. Cache trajectories, track energy with codecarbon, sync trajectories back to the laptop.

## Phase 4 — Evaluation + ablation (Weeks 10-13)
Score AURC (primary), ECE (15-bin), Brier, AUROC, selective accuracy @ 50/70/90% with bootstrap CIs (B=1000), TrustSQL Reliability Score @ penalties {1, N/2, N}. Paired bootstrap, alpha=0.05, Bonferroni across four mechanisms. M4 feature-group ablation. Original vs community-corrected BIRD. Generate plots. Publish to GitHub + Zenodo DOI.

## Phase 5 — Writing (Weeks 14-16)
Draft all chapters in Sonia's own voice; integrate figures, tables, and appendices (prompts, seeds, model versions, compute budget). Finalize.
