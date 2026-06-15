# ICLR Main Gate

Paper: 118 world_model_audits_from_failed_rollouts

Previous v3 decision: KILL_ARCHIVE

V4 gate verdict: STRONG_REVISE

Evidence digest:

- Proposed success: `0.717 +/- 0.007`.
- Strongest non-oracle baseline: `active_probe_planner` at `0.609 +/- 0.006`.
- Paired difference: `0.109 +/- 0.010`, wins `7/7`.
- Mechanism-F1 delta: `+0.175`.
- Invalid-repair delta: `-0.079`.
- Repeat-failure delta: `-0.083`.
- Damage-rate delta: `-0.022`.
- Diagnostic-probe cost delta: `-0.077`.
- Best ablation gap: `0.054`.

Gate result: all local gates pass.

ICLR main ready: no. External validation and real robot or accepted high-fidelity simulator evidence are still missing.
