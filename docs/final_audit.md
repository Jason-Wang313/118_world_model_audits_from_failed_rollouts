# Final Audit

Submission-hardening version: v4.1

Decision: STRONG_REVISE

The v4.1 rebuild clears the local evidence gate. The proposed failed-rollout audit beats the strongest non-oracle baseline, `active_probe_planner`, by `0.109 +/- 0.010` success under combined stress with 7/7 paired seed wins. It also improves mechanism localization and reduces invalid repairs, repeat failures, damage, and diagnostic-probe cost.

Continuation audit additions:

- Stress sweep coverage: `10,080` task/regime/seed rows and `30` aggregate rows.
- Failure cases: `8` documented failed-rollout audit boundaries.
- Numeric integrity: no NaN or infinite values found across result CSVs.
- Canonical PDF: `C:/Users/wangz/Downloads/118.pdf`.
- PDF SHA256: `E177208F2B36F64421AF5E87C3BA090BBD56F63D2F5A111807E9049657240761`.
- PDF size: `305247` bytes.
- Desktop PDF copy: absent.

The paper is not ICLR-main ready yet. Missing items remain:

- real robot validation;
- external high-fidelity simulator validation;
- independent implementation of all major baselines;
- videos or qualitative rollouts;
- full manual related-work synthesis beyond the hostile-pool slice.

Recommended action: keep as a serious submission rebuild candidate, not as a camera-ready main-conference paper.
