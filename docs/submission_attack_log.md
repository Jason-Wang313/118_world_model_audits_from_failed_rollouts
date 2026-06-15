# Submission Attack Log

## Attack 1: Strongest baseline selection

Mitigation: the strongest non-oracle baseline is selected by combined-stress success after generation. It is `active_probe_planner`.

## Attack 2: Success-only claim

Mitigation: the paper reports mechanism F1, invalid repair, repeat failure, damage, probe cost, calibration error, paired-seed wins, ablations, and stress sweeps.

## Attack 3: Decorative components

Mitigation: removing active probes, repair memory, counterfactual replay, failure traces, mechanism taxonomy, or the full audit objective reduces combined-stress success.

## Attack 4: Overclaiming ICLR readiness

Mitigation: all docs and the manuscript state `STRONG_REVISE`, not ICLR-main-ready. Real robot or external high-fidelity validation remains required.

## Attack 5: Thin stress/failure audit

Mitigation: v4.1 expands `stress_sweep_seed_metrics.csv` to `10,080` task/regime/seed rows and `failure_cases.csv` to `8` documented failed-rollout audit boundaries.
