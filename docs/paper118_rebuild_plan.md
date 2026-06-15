# Paper 118 Rebuild Plan

Started: 2026-06-15 03:49:00 +0100

## Goal

Rebuild `world_model_audits_from_failed_rollouts` from an archive memo into a real local empirical submission package. The paper must test whether failed robot rollouts can be converted into mechanism-localized audits of missing world-model assumptions, then used to repair planning decisions under physical shift.

## Claim To Test

Generic uncertainty and risk filters often identify that a rollout is risky without identifying which physical assumption failed. A failed-rollout audit should assign each failure to an action-critical missing mechanism, such as friction, compliance, occlusion persistence, contact mode, actuator lag, or payload shift, and then use the audit to choose safer diagnostic probes or repairs.

## Evidence Design

- Benchmark dimensions: 6 manipulation/control task families, 8 hidden physical failure regimes, 5 deployment splits, 9 controllers/auditors, 7 paired seeds, 72 rollout episodes per group.
- Methods: observed-only planner, data augmentation, scalar uncertainty planner, ensemble disagreement planner, conformal risk filter, failure-classifier repair, active probe planner, proposed failed-rollout mechanism audit, and oracle mechanism audit.
- Metrics: task success, mechanism-localization F1, invalid repair rate, repeat-failure rate, damage rate, diagnostic probe cost, calibration error, and paired-seed wins.
- Stress sweep: increasing hidden-mechanism ambiguity and observation sparsity.
- Ablations: remove failure traces, remove mechanism taxonomy, remove counterfactual replay, remove active probes, remove repair memory, and risk-only audit.

## Terminal Gates

The paper may become `STRONG_REVISE` only if all gates clear against the strongest non-oracle baseline:

- Combined-stress success margin is at least 0.030.
- Mechanism-localization F1 improves by at least 0.040.
- Invalid repair rate decreases by at least 0.020.
- Repeat-failure rate decreases by at least 0.020.
- Damage rate decreases by at least 0.010.
- Diagnostic probe cost does not increase.
- Paired-seed success wins are at least 5/7.
- Best ablation trails the full method by at least 0.020.

If any gate fails, the terminal decision remains `KILL_ARCHIVE` with the negative result documented.
