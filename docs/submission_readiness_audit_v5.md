# Submission Readiness Audit v5

Paper: 118 `world_model_audits_from_failed_rollouts`

Date: 2026-06-23

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py scripts\generate_manuscript.py scripts\validate_submission_artifacts.py
python src\run_experiment.py
python scripts\generate_manuscript.py
```

## Integrity Gates

- `dataset_summary.csv`: 240 rows
- `cell_metrics.csv`: 230,400 rows
- `main_group_metrics.csv`: 2,880 rows
- `seed_metrics.csv`: 600 rows
- `metrics.csv`: 12 rows
- `hard_seed_metrics.csv`: 120 rows
- `hard_aggregate_metrics.csv`: 12 rows
- `hard_pairwise_stats.csv`: 11 rows
- `ablation_cell_metrics.csv`: 38,400 rows
- `ablation_seed_metrics.csv`: 100 rows
- `ablation_metrics.csv`: 10 rows
- `stress_sweep_cell_metrics.csv`: 161,280 rows
- `stress_sweep_seed_metrics.csv`: 420 rows
- `stress_sweep.csv`: 42 rows
- `fixed_budget_cell_metrics.csv`: 107,520 rows
- `fixed_budget_seed_metrics.csv`: 280 rows
- `fixed_budget_metrics.csv`: 28 rows
- `fixed_budget_pairwise_stats.csv`: 24 rows
- `failure_cases.csv`: 24 rows
- Numeric sanity: validator found no NaN or infinite values.

## Result Gates

- Hard success margin: `0.09969`
- Hard utility margin: `0.26368`
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
- Stress endpoint success margin: `0.14401`
- Strict fixed-budget coverage: `0.62552`
- Strict fixed-budget breach: `0.00000`

All local gates pass.

## Artifact Gate

- Canonical PDF: `C:/Users/wangz/Downloads/118.pdf`
- PDF pages: 28
- PDF SHA256: `2AC788263369C553819D52E8E6715D108901635A944E4783E39044A506C58C11`
- PDF size: `728828` bytes
- Desktop PDF copy: absent
- LaTeX/BibTeX scan: no undefined citations, no warning/error/overfull matches in final scan; BibTeX reports `warning$ -- 0`.
- Visual PDF QA: pages 1, 4, 8, 14, 21, and 28 inspected.

## Submission Decision

The local evidence clears the expanded-standard strong-revise gate. The paper is not ICLR-main ready until external robot or accepted high-fidelity evidence, released artifacts, independent baselines, videos, calibrated logs, and a full manual related-work synthesis exist.
