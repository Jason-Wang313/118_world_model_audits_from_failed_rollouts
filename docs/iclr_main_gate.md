# ICLR Main Gate

Paper: 118 `world_model_audits_from_failed_rollouts`

v5 gate verdict: STRONG_REVISE

ICLR main ready: no

## Local Evidence Digest

- Proposed method: `counterfactual_mechanism_audit_v5`
- Strongest non-oracle baseline: `proposed_failed_rollout_audit_v4_1`
- Hard success: `0.80583` proposed vs `0.70615` baseline
- Hard utility: `0.68463` proposed vs `0.42095` baseline
- Mechanism-F1 delta: `+0.08835`
- Invalid-repair delta: `-0.04046`
- Repeat-failure delta: `-0.03822`
- Damage-rate delta: `-0.01269`
- Diagnostic-probe cost delta: `-0.03908`
- Calibration-error delta: `-0.01950`
- Budget-violation delta: `-0.05457`
- Paired hard utility wins: `10/10`
- Ablation success margin: `0.02135`
- Ablation utility margin: `0.04107`
- Max-stress success margin: `0.14401`
- Strict fixed-budget coverage: `0.62552`
- Strict fixed-budget breach: `0.00000`
- Failure cases: `24`

## Gate Result

All frozen local empirical gates pass.

## Scope Failure

The paper is not ICLR-main ready. It still lacks real robot rollouts, accepted high-fidelity robot world-model simulation, released world-model or policy checkpoints, calibrated contact-force/camera/state logs, hardware rollout videos, independent baseline implementations, and complete manual related-work synthesis.
