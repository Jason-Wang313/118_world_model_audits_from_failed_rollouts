# Final Audit

Decision: STRONG_REVISE

The v4 rebuild clears the local evidence gate. The proposed failed-rollout audit beats the strongest non-oracle baseline, `active_probe_planner`, by `0.109 +/- 0.010` success under combined stress with 7/7 paired seed wins. It also improves mechanism localization and reduces invalid repairs, repeat failures, damage, and diagnostic-probe cost.

The paper is not ICLR-main ready yet. Missing items remain:

- real robot validation;
- external high-fidelity simulator validation;
- independent implementation of all major baselines;
- videos or qualitative rollouts;
- full manual related-work synthesis beyond the hostile-pool slice.

Recommended action: keep as a serious submission rebuild candidate, not as a camera-ready main-conference paper.
