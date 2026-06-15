# Experiment Rigor Checklist

- [x] Paper-specific benchmark replacing the shared v3 template.
- [x] 6 task families, 8 hidden physical regimes, 5 deployment splits.
- [x] 9 controllers/auditors including strong non-oracle baselines and an oracle upper bound.
- [x] 7 paired seeds with 72 rollout episodes per group.
- [x] Strongest-baseline comparison selected by combined-stress success.
- [x] Paired-seed statistics reported for all baselines.
- [x] Mechanism metrics beyond success: mechanism F1, invalid repair, repeat failure, damage, probe cost, calibration error.
- [x] Ablations for failure traces, mechanism taxonomy, counterfactual replay, active probes, repair memory, and risk-only audit.
- [x] Stress sweep over hidden-mechanism ambiguity and observation sparsity with task/regime/seed detail.
- [x] Eight failure cases documented.
- [x] Terminal gates computed in `results/summary.txt`.

Residual risk: all evidence remains local and synthetic/deterministic. Real robot or external high-fidelity validation is still required before an ICLR-main submission claim.
