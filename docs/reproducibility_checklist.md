# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`
- Manuscript entry point: `scripts/generate_manuscript.py`
- Validator: `scripts/validate_submission_artifacts.py`
- Requirements: `numpy`, `matplotlib`
- Deterministic base seed: `11820265`
- Main outputs:
  - `results/cell_metrics.csv` with 230,400 rows
  - `results/main_group_metrics.csv` with 2,880 rows
  - `results/seed_metrics.csv` with 600 rows
  - `results/hard_aggregate_metrics.csv` with 12 rows
  - `results/hard_pairwise_stats.csv` with 11 rows
  - `results/ablation_cell_metrics.csv` with 38,400 rows
  - `results/stress_sweep_cell_metrics.csv` with 161,280 rows
  - `results/fixed_budget_cell_metrics.csv` with 107,520 rows
  - `results/failure_cases.csv` with 24 rows
  - `results/summary.json`
- Main figures:
  - `figures/world_model_audit_hard_success_v5.png`
  - `figures/world_model_audit_utility_budget_v5.png`
  - `figures/world_model_audit_ablation_v5.png`
  - `figures/world_model_audit_stress_sweep_v5.png`
  - `figures/world_model_audit_fixed_budget_v5.png`
  - `figures/world_model_audit_fixed_coverage_v5.png`

Reproduction command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py scripts\generate_manuscript.py scripts\validate_submission_artifacts.py
python src\run_experiment.py
python scripts\generate_manuscript.py
```

Residual risk: all evidence remains local and synthetic/deterministic. Real robot or accepted high-fidelity validation is still required before an ICLR-main submission claim.
