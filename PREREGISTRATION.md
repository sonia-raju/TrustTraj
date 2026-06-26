# PREREGISTRATION.md — Pre-Registered Methodology

> **DRAFT — decisions 1, 2, 3, 5 finalized; hypotheses H1–H4 awaiting wording confirmation. Lock only after hypotheses are confirmed. Must be locked before any experiment runs.**
>
> Methodology freezes at the end of Week 6. After the lock date, any deviation from a pre-registered element must be documented here (with reason) AND in DECISIONS.md before the change is implemented. Changes after lock must be labelled clearly as post-hoc deviations in the thesis.

---

## Title and Study Type

**Title:** Calibrated Abstention in Multi-Step LLM Agents: A Trajectory-Aware Reliability Layer for Text-to-SQL Analytics

**Study type:** Design-and-experiment study. A model-independent abstention layer is designed, implemented on top of an existing open agent framework, and evaluated through a controlled offline experiment. All four abstention mechanisms are scored post-hoc on the same recorded agent trajectories — the agent is run once per question, and mechanism scores are computed afterwards. This ensures a fair, internally valid comparison.

---

## Research Questions and Hypotheses (RQ1–RQ4)

The four research questions are taken verbatim from the approved thesis proposal.

**RQ1:** Do trajectory-level features, like how stable each step is, how steps interact with each other, and the characteristics of the structure, lead to a meaningful improvement in AURC and ECE compared to just using the confidence from the last step or the final answer in a text-to-SQL system?

**RQ2:** With a TrustSQL-like penalty score, does including a calibrated abstention layer make the overall reliability better than making the agent answer every time? Also, how much does the best answer/abstain threshold change with the penalty growth?

**RQ3:** Can a method called "conformal-abstention," which is taken from single-turn QA (Yadkori et al., 2024) be used for multi-step agents while still keeping its guarantee of coverage without relying on distribution, based on a small set of data that is set aside?

**RQ4:** How strong is the calibrated abstention layer when it comes to changes in (a) the basic open-weight LLM and (b) the type of database schema — meaning, can the calibrator adapt to different situations, or does it need to be adjusted for each specific (model × domain)?

---

### Directional Hypotheses H1–H4

> **>>> HYPOTHESES — DRAFT, awaiting confirmation of wording before lock.**
>
> Each hypothesis is mapped explicitly to its RQ, names the specific mechanism(s) compared, states the metric, and gives the predicted direction. Sonia must read each one and confirm or revise the wording before this document is locked.

**H1** (maps to RQ1 — trajectory-level features vs. end-only confidence):
M4 (trajectory-feature logistic calibrator, using cross-step dynamics, intra-step stability, positional, and structural features) will achieve a **lower AURC** and **lower ECE** on the held-out test set than M1 (end-only token log-probability threshold), and will achieve **higher selective accuracy** than M1 at matched coverage levels (50%, 70%, 90%). Predicted direction: M4 > M1 on all three metrics, indicating that trajectory-level features carry meaningful calibration signal beyond what the final-answer log-probability alone provides in a text-to-SQL setting.

**H2** (maps to RQ2 — TrustSQL reliability with abstention vs. always-answer; threshold shift with penalty):
Part A: Each calibrated abstention mechanism (M1, M2, M3, M4) will achieve a **higher TrustSQL Reliability Score** than a no-abstention baseline (always-answer) on the full TrustSQL test set (2,830 pairs), at least at one penalty level c ∈ {1, N/2, N}. Predicted direction: abstaining on genuinely infeasible questions improves the penalty-weighted reliability score. Part B: The optimal answer/abstain threshold for each mechanism will become **more conservative** (higher abstention fraction) as c increases from 1 to N/2 to N. Predicted direction: higher penalty increases the cost of wrong answers relative to abstentions, shifting the optimal threshold toward more frequent abstention.

> *Note: RQ2 has two parts (reliability improvement AND threshold sensitivity). H2 covers both. If Part A and Part B need to be tested separately for statistical reporting, they should be split into H2a and H2b at lock time — flag for Sonia.*

**H3** (maps to RQ3 — conformal coverage guarantee on multi-step trajectories):
M3 (conformal abstention with self-evaluation similarity scoring) will **maintain its distribution-free coverage guarantee** when applied to multi-step agent trajectories: the empirical error rate among answered questions on the held-out test set will **not exceed** the pre-specified target α = 0.10. Predicted direction: the empirical error rate ≤ 0.10 (guarantee holds). A violation — empirical error rate > 0.10 — would constitute a notable finding about the boundary conditions of conformal abstention in the agentic setting and will be reported as such. Sensitivity analysis at α = 0.05 and α = 0.20 (see M3 section) provides further evidence about guarantee tightness.

**H4** (maps to RQ4 — robustness across models and schema domains):
Part A (model robustness): When the M4 calibrator is trained on trajectories from Llama-3.1-8B-Instruct and applied without re-fitting to trajectories from Qwen-2.5-Coder-7B, the **AURC will be measurably higher** (worse) than when M4 is trained and evaluated on the same model's trajectories. Predicted direction: cross-model transfer degrades AURC, indicating partial model-dependence. Part B (domain robustness): Mechanisms evaluated on questions from database domains not seen during calibration (tested via a leave-one-database-out split as a secondary analysis) will show **higher AURC** than within-domain evaluation. Predicted direction: calibration is partially domain-dependent, consistent with HTC's finding of ECE degradation on out-of-domain tasks (Zhang, Xiong, et al., 2026).

> *Note: H4 is genuinely exploratory — the proposal frames RQ4 as an open question about whether the calibrator generalises. Parts A and B are best-effort directional predictions grounded in HTC's out-of-domain results; a null finding (no degradation on cross-model or cross-domain transfer) would be equally interesting and should be reported clearly.*

---

## Models

**Primary open-weight models** (both accessed via Hugging Face; exact revision hashes to be recorded at experiment time):
- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen2.5-Coder-7B-Instruct`

**Optional proprietary endpoint** (budget-dependent; only if EUR 150 API cost cap permits):
- GPT-4o-mini via OpenAI API (preferred), or Claude Haiku as fallback.
- Evaluated on a **separate set of 100 items only** to keep API costs controlled.
- The 100-item set is drawn from the same pre-registered BIRD subset (see Benchmarks).
- If the optional model is run, the exact API model-version string returned by the API must be logged.

**Constraint:** All primary experiments use open-weight models so the approach is broadly reproducible without proprietary API access.

---

## Benchmarks and Sampling

### Primary benchmark: BIRD-mini-dev

BIRD-mini-dev is a curated subset of BIRD (Li et al., 2023), which comprises 12,751 text-to-SQL pairs across 95 databases spanning 37 professional domains. It is chosen because its realistic, messy data and complex queries expose calibration weaknesses. Human-performance ceiling on the full benchmark is 92.96% EX; the current best published system reaches 81.67% EX.

A **pre-registered subset** of up to 300 questions will be drawn from BIRD-mini-dev using the procedure below. This subset is fixed before any model is run and is recorded here as part of the pre-registration.

**Locked selection procedure:**

- Target: N = 300, drawn with **equal allocation of 100 per difficulty tier** (simple / moderate / challenging — BIRD's three native difficulty labels).
- Method: filter by tier → shuffle with **selection seed 42** → take the first 100 (or all items if fewer than 100 exist in that tier). Do **not** backfill from other tiers if a tier is short.
- The tier labels used are BIRD's own `difficulty` field values. No re-labelling.

**Per-tier availability (BIRD-mini-dev):**

> ⚠️ Exact per-tier counts must be verified at data download time and entered here before any model run. The `data/` directory is not yet populated. Based on published reports, BIRD-mini-dev contains approximately 500 questions; all three tiers are expected to have ≥ 100 items, making the realized total N = 300. If any tier contains fewer than 100 items, the realized count for that tier is taken as-is and the realized total N (which may be less than 300) is recorded here.

| Tier | Available in BIRD-mini-dev | Sampled | Realized count |
|---|---|---|---|
| simple | TBD at download | min(100, available) | TBD |
| moderate | TBD at download | min(100, available) | TBD |
| challenging | TBD at download | min(100, available) | TBD |
| **Total** | **TBD** | **≤ 300** | **TBD** |

*Fill in the "Available" and "Realized count" columns at data download time, before running any model.*

Results will be reported on **both the original BIRD-mini-dev labels and community-corrected labels** (Ma et al., 2026 report 52.8% annotation error rate in BIRD Mini-Dev; relative performance shifts of −7% to +31% after correction). This dual reporting is pre-registered as a validity check, not a post-hoc adjustment.

### Secondary benchmark: TrustSQL

The full TrustSQL test set: 2,830 pairs (feasible and infeasible) from ATIS (794 pairs), Advising (918 pairs), and EHRSQL (1,118 pairs). 1,415 of the 2,830 items are infeasible (missing-schema, ambiguous, or non-SQL questions). Used to report the TrustSQL Reliability Score and to directly test RQ2. The full set is used without sub-sampling.

### Validation: Spider

Spider (Yu et al., 2018) is used as a simple validation / sanity check only — not as a primary evaluation benchmark. It will be run if compute allows and reported in an appendix.

---

## Abstention Mechanisms (M1–M4)

All four mechanisms are implemented and scored **post-hoc on the same recorded agent trajectories**. The agent is run once per question; the choice of abstention mechanism cannot influence trajectory generation. This is a core internal-validity guarantee.

| ID | Mechanism | Source |
|---|---|---|
| M1 | End-only token log-probability threshold (final answer step only) | Baseline; (Maleki et al., 2025) |
| M2 | Self-consistency / sampled agreement (k = 5), without a conformal layer | (Yadkori et al., 2024) |
| M3 | Conformal abstention with self-evaluation similarity scoring | (Yadkori et al., 2024) |
| M4 | Trajectory-feature logistic calibrator (reduced HTC; L1-regularised; ~12-20 features) | Based on (Zhang, Xiong, et al., 2026) |

### M1 — End-only log-probability threshold

The mean token log-probability of the final SQL answer step is used as the confidence score c(T). A threshold τ is chosen to minimise AURC on the calibration split (grid search over the empirical score distribution). g(T) = 1 (answer) if c(T) ≥ τ, else g(T) = 0 (abstain).

### M2 — Self-consistency (k = 5)

The agent is sampled k = 5 times per question (with temperature > 0). The confidence score is the fraction of samples that produce the same SQL execution result as the majority answer. No conformal layer is applied. g(T) is determined by thresholding this agreement score on the calibration split.

### M3 — Conformal abstention with self-evaluation

Following Yadkori et al. (2024): the model generates a self-evaluation score (e.g., semantic similarity between a self-generated critique and a reference answer, or a prompted self-rating). Conformal calibration is applied on the calibration set to select a threshold that controls the error rate at the pre-specified level α. The resulting abstention policy has a distribution-free coverage guarantee conditional on the calibration set size.

**Locked conformal target error rate:**

- **Primary α = 0.10** — the conformal mechanism targets a maximum 10% error rate among answered questions (i.e., at least 90% coverage of answered questions are correct). This is the result reported in all main-results tables.
- **Sensitivity analysis (pre-registered robustness checks):** M3 is also evaluated at α = 0.05 and α = 0.20. These are reported alongside the primary result to show how coverage and abstention rate change with α. They are robustness checks, not additional primary analyses.

> Note: α = 0.10 here is the conformal error rate parameter for M3 only. It is entirely distinct from the α = 0.05 significance level used in the paired bootstrap statistical tests across mechanisms.

### M4 — Trajectory-feature logistic calibrator

Inspired by HTC (Zhang, Xiong, et al., 2026), which uses a 48-dimensional feature vector. This thesis uses a reduced set of ~12–20 features drawn from four categories:

- **Cross-step dynamics:** how signals change between consecutive agent steps (e.g., log-prob trend, score variance across steps)
- **Intra-step stability:** consistency within a single step across k samples (e.g., per-step agreement rate)
- **Positional indicators:** where in the trajectory uncertainty peaks (e.g., step index of minimum log-prob, normalised position of first retry)
- **Structural attributes:** metadata about the trajectory shape (e.g., total step count, retry count, executor return code, whether a schema-lookup was invoked)

A L1-regularised logistic regression is fit on the calibration split. L1 is chosen for interpretability — the proposal cites Marchal et al. (2026) on the importance of trust through transparency.

**Locked core feature set (8 features, guaranteed regardless of scope reduction):**

These 8 features — two per category — are pre-registered and will be included in every M4 run. The full feature list of ~12–20 will be finalised at the Week-6 scope freeze, once the trajectory logging code is implemented and it is confirmed which signals are reliably computable. At Week 6, the complete list must be written here (or in a linked document) before any experiment is run. The four categories are fixed now and cannot be changed after lock.

| # | Category | Feature | Description |
|---|---|---|---|
| 1 | Cross-step dynamics | Confidence-trajectory slope | Linear regression slope of per-step mean log-probability across the K steps of the trajectory. Negative slope = falling confidence. |
| 2 | Cross-step dynamics | Semantic drift | Normalised edit distance (or embedding cosine distance) between successive candidate SQL queries across steps; measures how much the agent's answer changes. |
| 3 | Intra-step stability | Final-step self-consistency | Fraction of k sampled candidates at the final step that produce the same execution result as the chosen answer (shared with M2's k=5 samples). |
| 4 | Intra-step stability | Final-step mean log-probability | Mean token log-probability of the chosen SQL query at the final step (shared with M1's confidence score). |
| 5 | Positional | Trajectory length | Total number of agent steps K to the terminal answer. |
| 6 | Positional | Stabilisation step index | The step index at which the final SQL query first appeared and was not subsequently changed; normalised by K. |
| 7 | Structural | SQL complexity | Count of JOIN clauses plus nested subqueries in the final SQL query. |
| 8 | Structural | Schema-linking coverage | Fraction of tables and columns referenced in the final SQL that are present in the database schema. |

> **Leakage guard:** Any execution-derived signal (e.g., SQL parse success, execution success/failure return code) is treated strictly as a predictor feature and is **never** mixed into the correctness label used to train or evaluate M4. The correctness label is always derived from comparing the execution result set against the gold answer, independently of any feature value.

**Feature ablation:** M4 is also evaluated with one feature group removed at a time (four ablated variants), to quantify each group's contribution. This is Specific Objective 4 from the proposal.

---

## Evaluation Metrics

### Primary metric
- **AURC** (Area Under the Risk-Coverage curve): the lower the better. This is the main metric for comparing M1–M4.
- **Risk-coverage curves** are always plotted alongside AURC.

### Secondary metrics
- **ECE** (Expected Calibration Error): 15-bin reliability diagrams; lower is better.
- **Brier score:** lower is better; reported as a robustness check on ECE.
- **Adaptive-bin ECE:** robustness check (equal-mass bins).
- **AUROC:** measures how well confidence scores discriminate correct from incorrect answers; higher is better.
- **Selective accuracy at 50%, 70%, and 90% coverage:** with bootstrap 95% CIs (B = 1,000 bootstrap samples). The test statistic is the difference in selective accuracy between each mechanism and M1 (the baseline).
- **TrustSQL Reliability Score** at penalty levels c ∈ {1, N/2, N}, where N = total test-set items. Reported on the full TrustSQL test set (2,830 pairs).
- **Abstention precision:** fraction of abstentions that were on genuinely incorrect answers.
- **Abstention recall:** fraction of incorrect answers that were correctly abstained on.

### Agentic task metrics (BIRD only)
- **Execution accuracy (EX):** fraction of answered questions where the generated SQL produces the correct result set. Reported broken down by BIRD difficulty level (easy/medium/hard/extra-hard).
- **Valid Efficiency Score (VES):** BIRD's efficiency metric.

---

## Seeds

Random seeds **{0, 1, 2}** are used for all randomness: model temperature sampling, data shuffling (if any), and train/calibration/test splits.

All three seeds are run for the two primary open-weight models, giving a 2 models × 3 seeds = 6 trajectory sets for the primary analysis. The optional GPT-4o-mini run uses seed 0 only (100-item set).

Seeds are set at the top of every script using:
```python
import random, numpy as np
random.seed(SEED)
np.random.seed(SEED)
# torch.manual_seed(SEED) if PyTorch is used
```

Hugging Face model revision hashes (not just model names) are recorded for full reproducibility.

---

## Calibration / Test Split

**Locked split procedure:**

- **Ratio:** 50 / 50 (calibration set / held-out test set).
- **Stratification:** the split is stratified by difficulty tier (simple / moderate / challenging), so both halves preserve the same tier balance as the full pre-registered subset.
- **Split seed:** 7 (separate from model-run seeds {0,1,2} and selection seed 42).
- **Created once:** the split is generated once from the pre-registered question indices, before any trajectory is generated or examined.
- **Shared across all mechanisms:** the identical calibration/test split is applied to M1, M2, M3, and M4. This is what makes the **paired bootstrap valid** — all four mechanisms are scored on exactly the same held-out test questions.

**Role of each half:**

| Split half | Used for |
|---|---|
| Calibration set (50%) | Fit the M4 L1-regularised logistic calibrator. Set the abstention threshold τ for M1 and M2 (grid search to minimise AURC on calibration data). Run conformal calibration for M3 (select threshold to control error rate at α = 0.10 on calibration data). |
| Held-out test set (50%) | Compute and report **all** metrics: AURC, ECE, Brier, AUROC, selective accuracy at 50/70/90%, TrustSQL Reliability Score, abstention precision/recall, EX, VES. No tuning or threshold adjustment is permitted on the test set. |

With N ≈ 300 questions, each half contains ~150 questions. Across 3 seeds, the effective test-set size for bootstrap CIs is 150 × 3 = 450 trajectory-level observations per model.

---

## Statistical Analysis

- **Method:** Paired bootstrap on shared recorded trajectories. The agent is run once per question; mechanisms are scored post-hoc on the identical trajectory. This eliminates trajectory-generation variance from the mechanism comparison.
- **Significance level:** α = 0.05 (two-tailed).
- **Multiple comparisons:** Bonferroni correction across the four mechanisms. With 4 mechanisms compared pairwise to M1 (the baseline), the corrected threshold is α / 4 = 0.0125.
- **Bootstrap samples:** B = 1,000 for all bootstrap CIs (selective accuracy, AURC differences).
- **Reporting:** All results include point estimates and 95% bootstrap CIs. Effect sizes are reported alongside p-values. Non-significant results are reported as such; they are not treated as failures.

---

## Scope Freeze Date (Week 6)

The project scope — benchmarks, subset selection, models, abstention mechanisms, evaluation metrics, and the M4 feature list — freezes at the **end of Week 6** of the thesis timeline.

After the freeze date:
1. No new mechanisms may be added.
2. No metrics may be added as primary metrics (secondary metrics may be added if they do not change the primary conclusions).
3. Any change to a pre-registered element requires a dated entry in both PREREGISTRATION.md (under "Post-Registration Deviations") and DECISIONS.md.
4. The freeze date (calendar date) will be entered here once the thesis start week is confirmed.

> **Freeze calendar date:** TBD — enter absolute date once Week 1 start date is known.

---

## Negative-Result Plan

Pre-registered explicitly (from the proposal):

If **M4 does not outperform M1, M2, or M3** on the primary metric (AURC), this is treated as a scientifically valid outcome. The thesis will:

1. Report the negative finding clearly and without hedging, alongside all secondary metrics and ablation results.
2. Publish the full evaluation tool, recorded trajectories, and scoring scripts under an open license — itself a reusable scientific contribution.
3. Interpret the result: if M4 does not beat M3 (conformal abstention), this provides evidence that distribution-free conformal abstention is the preferable default for agentic analytics, and the thesis will argue this case explicitly.
4. The feature ablation (M4 variants) will still be reported to show which trajectory feature groups are informative even if the combined M4 does not beat simpler baselines.

The negative-result plan was designed into the proposal: "The contribution is designed to be robust to a null result" (Strengths §2).

---

## Post-Registration Deviations

*(This section is empty until a deviation is made. Any post-lock change is recorded here with date, what changed, why, and reference to the DECISIONS.md entry.)*

---

## Lock Date

**Not yet locked.**

To lock: Sonia confirms the wording of H1–H4 (the only remaining open item), then signs off with:

`Locked on YYYY-MM-DD by Sonia Raju. No further changes without a documented deviation recorded in this file and in DECISIONS.md.`
