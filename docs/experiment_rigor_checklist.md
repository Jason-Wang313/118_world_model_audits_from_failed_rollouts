# Experiment Rigor Checklist

- [x] Bulletproof plan written before execution.
- [x] Paper-specific v5 benchmark replacing the old scaffold.
- [x] 6 task families, 8 hidden physical mechanisms, 5 deployment splits.
- [x] 12 controllers/auditors including strong non-oracle baselines, previous-method baseline, and oracle upper bound.
- [x] 10 paired seeds with 8 rollout episodes per cell.
- [x] Strongest-baseline comparison selected by hard-slice repair utility.
- [x] Paired-seed statistics reported for all non-oracle baselines.
- [x] Mechanism metrics beyond success: mechanism F1, invalid repair, repeat failure, damage, probe cost, calibration error, abstention, budget violation, predicted breach, realized breach, and repair utility.
- [x] Ablations for failed-rollout traces, mechanism taxonomy, counterfactual replay, active probe value, repair memory, calibration gate, budget controller, freshness guard, and scalar-risk-only audit.
- [x] Stress sweep over hidden-mechanism ambiguity, observation sparsity, horizon pressure, repair cost, and miscalibration.
- [x] Fixed-budget deployment audit with coverage, breach, gated success, and gated utility.
- [x] 24 failure cases documented.
- [x] Terminal gates computed in `results/summary.json`.
- [x] 28-page PDF with bright boxed clickable citations.
- [x] Validator passed on the Downloads-only numbered PDF.

Residual risk: all evidence remains local and synthetic/deterministic. Real robot or accepted high-fidelity validation is still required before an ICLR-main submission claim.
