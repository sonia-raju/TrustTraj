# DECISIONS.md — Decision Record
Format: ID | Date | Decision | Rationale. Newest on top.

D3 | 2026-06-21 | Compute platform = Google Colab Pro for trajectory generation. | Simplest path for a beginner; reliable enough with output caching; well under the EUR 150 budget.
D2 | 2026-06-21 | Hybrid compute split: laptop = command center (dev, eval, writing); cloud GPU = trajectory generation. | Local hardware (MX250 2 GB VRAM, 8 GB RAM) cannot run 7-8B models; the proposal's record-once-score-offline design supports the split.
D1 | 2026-06-21 | Adopt the proposal's record-once-score-offline experimental design. | Lets all four mechanisms be scored fairly on identical recorded trajectories and enables the compute split.
