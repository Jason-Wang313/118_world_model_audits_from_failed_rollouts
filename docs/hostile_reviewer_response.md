# Hostile Reviewer Response

## Attack: This is just uncertainty estimation after failure.

Response: The benchmark separates scalar uncertainty, ensemble disagreement, conformal risk filtering, failure classification, active probing, and mechanism-localized auditing. The proposed method beats the strongest of these, `active_probe_planner`, by `0.109 +/- 0.010` success and improves mechanism F1 by `0.175`.

## Attack: The method may improve success by probing more.

Response: The proposed audit lowers diagnostic-probe cost by `0.077` relative to `active_probe_planner`, so the local gain is not explained by simply spending more probes.

## Attack: The mechanism taxonomy could be decorative.

Response: The `minus_mechanism_taxonomy` ablation drops from `0.719 +/- 0.006` to `0.619 +/- 0.005`, and the best removed-component ablation trails by `0.054`.

## Attack: The benchmark is still not enough for ICLR main.

Response: Agreed. The terminal decision is `STRONG_REVISE`, not final acceptance readiness. The v4.1 evidence has 10,080 detailed stress rows and 8 failure cases, but the work still needs real robot or external high-fidelity validation.
