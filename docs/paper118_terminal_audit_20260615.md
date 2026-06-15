# Paper 118 Terminal Audit - 2026-06-15

Paper: `world_model_audits_from_failed_rollouts`

Terminal state: STRONG_REVISE

ICLR main ready: no

## What Passed

- Code compiled with `python -m py_compile src\run_experiment.py`.
- Experiment reran successfully under low-RAM thread caps.
- All expected CSV row counts passed.
- Numeric audit found no NaN or infinite values.
- Proposed method beats the strongest non-oracle baseline under combined stress.
- Proposed method wins 7/7 paired seeds over the strongest non-oracle baseline.
- Mechanism localization F1 improves.
- Invalid repairs, repeat failures, damage, and diagnostic-probe cost decrease.
- Core ablations remain below the full method.
- Stress evidence now includes 10,080 task/regime/seed rows.
- Failure-case documentation now includes 8 concrete boundaries.
- Canonical PDF exists at `C:/Users/wangz/Downloads/118.pdf`.
- PDF SHA256 is `E177208F2B36F64421AF5E87C3BA090BBD56F63D2F5A111807E9049657240761`.
- PDF size is `305247` bytes.
- No copy exists at `C:/Users/wangz/Desktop/118.pdf`.
- LaTeX/BibTeX scan is clean except benign `rerunfilecheck`; BibTeX reports `warning$ -- 0`.

## What Did Not Pass

- No real robot validation.
- No external high-fidelity simulator benchmark.
- No trained world-model checkpoint release.
- No independent baseline implementations.
- No hardware videos or qualitative rollouts.
- Related work still needs manual full-paper synthesis.

## Decision

Mark as `STRONG_REVISE`. Do not claim ICLR-main submission readiness until real robot or independent high-fidelity validation gates are satisfied.
