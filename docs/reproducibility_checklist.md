# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`
- Requirements: `numpy`, `matplotlib`
- Deterministic base seed: `11840615`
- Main outputs:
  - `results/seed_task_regime_metrics.csv`
  - `results/seed_split_metrics.csv`
  - `results/metrics.csv`
  - `results/pairwise_stats.csv`
  - `results/ablation_metrics.csv`
  - `results/stress_sweep.csv`
  - `results/stress_sweep_seed_metrics.csv` with 10,080 detailed rows
  - `results/failure_cases.csv`
  - `results/summary.txt`
- Main figures:
  - `figures/world_model_audit_combined_success.png`
  - `figures/world_model_audit_diagnostics.png`
  - `figures/world_model_audit_stress_sweep.png`
  - `figures/world_model_audit_ablation.png`
  - `figures/world_model_audit_regime_gains.png`

Reproduction command:

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```
