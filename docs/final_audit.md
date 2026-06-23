# Final Audit

Paper: 118 `world_model_audits_from_failed_rollouts`

Expanded-standard version: v5

Terminal decision: STRONG_REVISE

ICLR main ready: no

The v5 package passes the local expanded-standard audit: deterministic runner, generated evidence, 28-page PDF, bright boxed clickable citations, clean BibTeX, Downloads-only numbered artifact, visual page QA, and validator checks.

Final PDF: `C:/Users/wangz/Downloads/118.pdf`

SHA256: `2AC788263369C553819D52E8E6715D108901635A944E4783E39044A506C58C11`

Reason for STRONG_REVISE: `counterfactual_mechanism_audit_v5` beats `proposed_failed_rollout_audit_v4_1` on hard success, utility, mechanism F1, invalid repair, repeat failure, damage, probe cost, calibration, budget violation, paired hard utility seeds, ablation, stress endpoint, and fixed-budget metrics.

Reason it is not ICLR-main ready: no real robot rollouts, accepted high-fidelity validation, released checkpoint, calibrated logs, rollout videos, independent baseline implementations, or complete manual related-work synthesis exist.
