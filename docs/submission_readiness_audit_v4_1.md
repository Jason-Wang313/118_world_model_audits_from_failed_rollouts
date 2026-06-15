# Submission Readiness Audit v4.1

Paper: 118 `world_model_audits_from_failed_rollouts`

Date: 2026-06-15

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

Command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\118_world_model_audits_from_failed_rollouts_continuation_rerun_20260615.log
```

## Integrity Gates

- `metrics.csv`: 9 rows.
- `per_task_regime_metrics.csv`: 432 rows.
- `seed_task_regime_metrics.csv`: 15,120 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 2,352 rows.
- `stress_sweep.csv`: 30 rows.
- `stress_sweep_seed_metrics.csv`: 10,080 task/regime/seed rows.
- `failure_cases.csv`: 8 rows.
- Numeric sanity: no NaN or infinite values found.

## Result Gates

- Strongest non-oracle baseline: `active_probe_planner`.
- Combined-stress success: `0.717 +/- 0.007` proposed vs `0.609 +/- 0.006` baseline.
- Paired success gain: `0.109 +/- 0.010`, 7/7 seed wins.
- Mechanism F1: `0.704` proposed vs `0.529` baseline.
- Invalid repair: `0.136` proposed vs `0.215` baseline.
- Repeat failure: `0.125` proposed vs `0.208` baseline.
- Damage rate: `0.062` proposed vs `0.083` baseline.
- Diagnostic probe cost: `0.242` proposed vs `0.319` baseline.
- Ablation margin over best removed component: `0.054`.
- Max stress success: `0.660 +/- 0.005` proposed vs `0.538 +/- 0.008` active probing and `0.784 +/- 0.003` oracle.

## Artifact Gate

- Canonical PDF: `C:/Users/wangz/Downloads/118.pdf`.
- PDF SHA256: `E177208F2B36F64421AF5E87C3BA090BBD56F63D2F5A111807E9049657240761`.
- PDF size: `305247` bytes.
- Desktop PDF copy: absent.
- LaTeX/BibTeX scan: clean except benign `rerunfilecheck`; BibTeX reports `warning$ -- 0`.

## Submission Decision

The local evidence clears the strong-revise gate: strongest-baseline margin, mechanism-F1 gain, invalid-repair/repeat-failure/damage/probe-cost reductions, paired-seed wins, ablation margin, expanded stress detail, and failure-case documentation all pass.

The paper is not ICLR-main ready. It still needs real robot or independent high-fidelity validation, trained world-model checkpoint release, independent baseline implementations, hardware/video artifacts, and deeper manual related-work synthesis before submission.
