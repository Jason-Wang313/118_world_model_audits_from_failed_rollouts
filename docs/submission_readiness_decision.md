# Submission Readiness Decision

Terminal decision: STRONG_REVISE

ICLR main ready: no

Why strong-revise:

- `0.109 +/- 0.010` success gain over the strongest non-oracle baseline.
- 7/7 paired seed wins.
- Mechanism-F1, invalid-repair, repeat-failure, damage, and probe-cost gates all pass.
- Best ablation trails the full method by `0.054`.
- Stress sweep and failure cases are included.

Why not ready:

- no real robot validation;
- no external high-fidelity simulator validation;
- no released trained world-model checkpoint;
- no independent baseline implementations;
- no qualitative rollout videos.
