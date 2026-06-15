# Claims

- Mechanism claim: failed rollouts are useful when they localize which physical assumption the world model missed, not merely when they raise scalar uncertainty.
- Evidence claim: the v4 benchmark tests mechanism-localized audits across hidden friction, compliance, occlusion persistence, contact-mode, actuator-lag, payload-shift, and combined hidden-mechanism regimes.
- Result claim: under combined stress, the proposed audit reaches `0.717 +/- 0.007` success versus `0.609 +/- 0.006` for `active_probe_planner`, with `0.109 +/- 0.010` paired success gain and 7/7 seed wins.
- Mechanism-diagnostic claim: the proposed audit improves mechanism F1 by `0.175`, lowers invalid repairs by `0.079`, lowers repeat failures by `0.083`, lowers damage by `0.022`, and lowers probe cost by `0.077`.
- Scope claim: the evidence supports `STRONG_REVISE`, not final ICLR-main readiness.
- Unsupported claim explicitly avoided: no claim of state-of-the-art robot world-model performance on real robots or external simulators.
