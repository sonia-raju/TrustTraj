# steplog.md — Append-Only Step Log
Purpose: a complete chronological record of every action (success or failure). Append only; never edit or delete. Format: `YYYY-MM-DD HH:MM | actor | action | result`.

2026-06-21 12:08 | Claude Code | Scaffolded repository (folders + governance files) | success
2026-06-21 12:20 | Claude Code | git confirmed installed and user identity configured; docs/ added to .gitignore | success
2026-06-26 21:35 | Claude Code | Python 3.11.7 (accidentally installed in D:\TrustTraj\) relocated to D:\Python311\; all runtime files moved, installer EXEs deleted, User PATH updated to D:\Python311 + D:\Python311\Scripts, project venv created at D:\TrustTraj\.venv pointing to D:\Python311 | success
2026-06-26 22:00 | Claude Code | BIRD-mini-dev dataset (minidev.zip, ~800MB) copied from D:\minidev into D:\TrustTraj\data\minidev; original zip and folder deleted from D:\ root; stray D:\.venv deleted | success
2026-06-26 22:15 | Claude Code | Created src/inspect_datasets.py (DATA_DIR fixed from data/bird to data/minidev); ran from project root with .venv Python; output: 500 records, 3 tiers (simple=148, moderate=250, challenging=102), 11 DBs, 0 missing fields, 0 missing DB files on disk | success
2026-06-21 12:35 | Claude Code | Git confirmed installed and configured; docs/ already in .gitignore; Step 1 committed | success
2026-06-21 13:10 | Claude Code | Read full thesis proposal PDF; rewrote PREREGISTRATION.md from proposal with 5 DECISION NEEDED blocks; not yet committed — awaiting Sonia review | success
2026-06-24 | Claude Code | Finalized PREREGISTRATION.md decisions: D1=BIRD N≤300 stratified 100/tier seed42; D2=50/50 split seed7 shared across M1-M4; D3=conformal alpha=0.10 primary + sensitivity at 0.05/0.20; D5=8 core M4 features locked across 4 categories with leakage guard; H1-H4 drafted awaiting wording confirmation; no commit yet | success
2026-06-26 11:00 | GitHub Copilot | Create `.venv` virtual environment in d:\TrustTraj | failed: `python` not found in PATH; attempted `python -m venv .venv`
2026-06-26 11:02 | GitHub Copilot | Create `.venv` virtual environment in d:\TrustTraj | success: used `py -3 -m venv .venv`
