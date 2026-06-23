# Paper 118 Expanded Submission Plan - 2026-06-23

Paper: `world_model_audits_from_failed_rollouts`

Target: expand the current 4-page v4.1 package into a 25+ page v5 hostile-review submission artifact with stronger theory, stronger experiments, real citations, bright boxed clickable citation links, and honest terminal status.

## Non-Negotiables

- Optimize for hostile-review survival, not pretty numbers.
- Use strong baselines and stress tests to expose weaknesses.
- Improve the method during development, then freeze the final v5 protocol and report all predefined results.
- Keep the implementation CPU-only and RAM-light.
- Keep `118.pdf` in Downloads only.
- Do not claim ICLR-main readiness without real robot or accepted high-fidelity validation.

## Planned v5 Contribution

`counterfactual_mechanism_audit_v5` converts failed rollouts into a mechanism posterior and an action decision: repair, probe, abstain, or use a conservative fallback. It adds calibrated abstention and freshness-checked repair memory on top of v4.1.

## Planned Theory

- Define the hidden-mechanism audit problem.
- Separate mechanism localization from scalar uncertainty.
- State a repair-dominance condition: a mechanism audit can beat scalar risk only when localization error and probe cost are below the expected invalid-repair reduction.
- State a failure condition: under indistinguishable aliased mechanisms, the method must abstain or probe rather than force a repair.
- Keep theory explanatory and bounded to the local simulator; no unsupported real-world theorem claims.

## Planned Experiments

- Main benchmark with cell-level evidence across tasks, regimes, splits, methods, seeds, and episodes.
- Hard-slice aggregate and pairwise seed tests.
- Ablation suite for every method component.
- Stress suite for ambiguity, sparsity, aliasing, repair cost, and calibration shift.
- Fixed diagnostic-probe budget suite.
- Calibration and mechanism-diagnosis audit.
- At least 24 failure cases.

## Planned Documentation

- Update `README.md`, `child_status.md`, `docs/claims.md`, `docs/iclr_main_gate.md`, `docs/novelty_decision.md`, `docs/submission_attack_log.md`, `docs/hostile_reviewer_response.md`, `docs/submission_readiness_decision.md`, `docs/final_audit.md`, and `docs/submission_version_log.md`.
- Delete stale v4.1-only terminal plan/audit files after v5 artifacts exist.
- Add a validation script as the final local source of truth.

## Final Gate

Paper 118 can be marked complete only after the 25+ page PDF, generated evidence, public GitHub commit, Downloads-only artifact placement, visual PDF QA, and root ledger updates all pass.
