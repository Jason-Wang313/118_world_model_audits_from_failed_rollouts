# Novelty Decision

Decision: locally supported but not submission-ready.

Novelty boundary: the paper should claim a failed-rollout mechanism audit for repair/probe/abstention decisions. It should not claim a new generic world model, a new broad benchmark, a state-of-the-art robot policy, or sim-to-real robustness.

The defensible v5 contribution is `counterfactual_mechanism_audit_v5`: a typed hidden-mechanism posterior, counterfactual replay term, diagnostic-probe value, repair-risk penalty, calibrated abstention gate, probe-budget controller, and repair-memory freshness guard.

The local evidence supports STRONG_REVISE because v5 beats the previous method and strong baselines under hard, ablation, stress, and fixed-budget gates. The external novelty and deployment claim remains unproven without real robot or accepted high-fidelity validation.
