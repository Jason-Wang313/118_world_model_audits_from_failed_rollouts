# Claims

- Mechanism claim: failed rollouts are useful when they localize which physical mechanism the world model missed, not merely when they raise scalar uncertainty.
- Method claim: `counterfactual_mechanism_audit_v5` uses a typed mechanism posterior, failed-rollout likelihood, counterfactual replay, diagnostic-probe value, repair-risk penalty, calibrated abstention, probe-budget control, and repair-memory freshness.
- Evidence claim: the v5 local suite contains `230,400` main rollout cells, `38,400` ablation cells, `161,280` stress cells, `107,520` fixed-budget cells, and `24` failure cases.
- Result claim: on the hard slice, v5 reaches `0.80583` success and `0.68463` utility versus `0.70615` success and `0.42095` utility for `proposed_failed_rollout_audit_v4_1`.
- Diagnostic claim: v5 improves mechanism F1 by `+0.08835`, invalid repair by `-0.04046`, repeat failure by `-0.03822`, damage by `-0.01269`, probe cost by `-0.03908`, calibration error by `-0.01950`, and budget violation by `-0.05457`.
- Scope claim: the evidence supports `STRONG_REVISE`, not final ICLR-main readiness.
- Unsupported claim explicitly avoided: no state-of-the-art real robot world-model performance or external simulator transfer claim is made.
