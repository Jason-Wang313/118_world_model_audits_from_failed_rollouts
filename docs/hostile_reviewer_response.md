# Hostile Reviewer Response

## Attack: This is just scalar uncertainty.

Response: v5 reports mechanism F1, invalid repair, repeat failure, damage, probe cost, calibration, budget violation, ablations, and fixed-budget gates. Scalar uncertainty baselines are included and beaten.

## Attack: The paper hides the previous method.

Response: the old proposed method is retained as `proposed_failed_rollout_audit_v4_1` and is the strongest non-oracle baseline.

## Attack: The method wins by over-probing.

Response: diagnostic-probe cost decreases by `-0.03908` against the strongest non-oracle baseline, and fixed-budget coverage/breach are reported.

## Attack: The method wins by abstaining.

Response: the fixed-budget audit reports coverage (`0.62552` at budget `0.10`), breach (`0.00000`), gated success (`0.78912`), and gated utility margin.

## Attack: The ablations are decorative.

Response: full v5 beats the strongest removed-component ablation by `0.02135` success and `0.04107` utility.

## Attack: Synthetic local results are not enough.

Response: agreed. The paper is marked `STRONG_REVISE`, not ICLR-main ready, until external robot or accepted high-fidelity validation and release artifacts exist.
