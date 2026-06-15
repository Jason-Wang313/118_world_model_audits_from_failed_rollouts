# 118 World-Model Audits From Failed Rollouts

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild replaces the archive scaffold with a paper-specific local benchmark for failed-rollout world-model audits. The v4.1 continuation audit expands stress and failure coverage while preserving the honest strong-revise direction: the proposed method converts failed robot rollouts into mechanism-localized diagnoses, then uses those diagnoses to choose repairs and diagnostic probes. It is not yet ICLR-main ready because it lacks real robot or external high-fidelity validation.

## Evidence Snapshot

- Design: 6 task families x 8 hidden physical regimes x 5 deployment splits x 9 controllers, 7 paired seeds, 72 rollout episodes per group.
- Strongest non-oracle baseline: `active_probe_planner`.
- Combined-stress success: proposed `0.717 +/- 0.007` vs baseline `0.609 +/- 0.006`.
- Paired difference: `0.109 +/- 0.010`, wins `7/7` seeds.
- Mechanism-F1 delta: `+0.175`.
- Invalid-repair delta: `-0.079`; repeat-failure delta: `-0.083`.
- Damage-rate delta: `-0.022`; diagnostic-probe cost delta: `-0.077`.
- Best ablation gap: `0.054`.
- Stress sweep coverage: `10,080` task/regime/seed rows plus `30` aggregate rows.
- Failure cases: `8` documented failed-rollout audit boundary cases.
- Latest rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/118_world_model_audits_from_failed_rollouts_continuation_rerun_20260615.log`.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/118.pdf`

PDF SHA256: `E177208F2B36F64421AF5E87C3BA090BBD56F63D2F5A111807E9049657240761`

PDF size: `305247` bytes.

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
