# Paper 118 Expanded-Standard v5 Plan

Goal: rebuild `world_model_audits_from_failed_rollouts` into a 25+ page, CPU-only, RAM-light, hostile-review submission package. The output remains honest: local evidence can justify `STRONG_REVISE`, but not ICLR-main readiness without real robot or independently accepted high-fidelity validation.

## Frozen Protocol

1. Keep the canonical numbered PDF at `C:/Users/wangz/Downloads/118.pdf` only.
2. Do not copy numbered PDFs to the Desktop, factory root, or child repo root.
3. Predefine all result gates before interpreting results.
4. Select the strongest non-oracle baseline automatically after the full run.
5. Report every predefined metric, including failed gates and negative cases.
6. Keep CPU/RAM usage light: deterministic NumPy/CSV generation, single-process execution, no large model downloads, no GPU assumptions.
7. Use real, checkable references and bright boxed clickable citation links in the PDF.

## Method Upgrade

Develop v5 as `counterfactual_mechanism_audit_v5`, not merely a renamed v4.1 script. The method must add:

- A typed hidden-mechanism variable for friction, compliance, occlusion persistence, contact-mode flip, actuator lag, payload shift, sensor dropout, and compound aliasing.
- A failed-rollout likelihood term, a counterfactual replay term, a diagnostic-probe value term, a repair-risk penalty, and a calibrated abstention gate.
- A probe-budget controller that can abstain, repair, probe, or fall back to a conservative controller under uncertain mechanism identity.
- A repair-memory freshness check to prevent stale failed-rollout memory from poisoning later regimes.
- A confidence/decomposition analysis explaining when mechanism-localized audits can improve repair decisions over scalar uncertainty.

## Experiment Upgrade

Run a new v5 suite with:

- Main benchmark: multiple task families, hidden physical regimes, deployment splits, controllers, seeds, and episodes with raw cell-level rows.
- Baselines: observed-only, data-augmented, scalar uncertainty, ensemble disagreement, conformal risk, failure classifier, active probing, causal-query baseline, latent-MPC/PETS-style baseline, v4.1 proposed baseline, v5 proposed, and oracle.
- Hard aggregate: combined hidden mechanisms, sparse observations, long horizons, high repair cost, and aliasing regimes.
- Paired-seed comparisons against every non-oracle baseline.
- Ablations: remove failed traces, taxonomy, counterfactual replay, active probes, repair memory, calibration gate, abstention, budget controller, and freshness guard.
- Stress sweeps: hidden-mechanism ambiguity, observation sparsity, counterfactual aliasing, repair-cost pressure, and model miscalibration.
- Fixed-budget deployment audit: strict diagnostic-probe budget with breach, coverage, utility, success, and abstention metrics.
- Calibration and diagnostic audit: mechanism F1, invalid repair, repeat failure, damage, probe cost, calibration error, abstention precision, and repair utility.
- Failure cases: at least 24 concrete boundary cases with lessons.

## Manuscript Upgrade

Generate a 25+ page ICLR-style PDF with:

- Abstract, contribution statement, claim/scope boundary, and hostile-review summary.
- Formal problem setup, method derivation, theory/intuition, and failure-mode analysis.
- Related work grounded in real world-model, model-based RL, robot benchmark, conformal-risk, and causal-confusion references.
- Tables and figures generated from v5 CSV outputs only.
- Explicit statement that the evidence is local/synthetic and not final ICLR-main-ready.
- Bright boxed clickable citations that jump to the bibliography.

## Validation Gates

The rebuild only counts as complete if all required artifacts pass:

- `python -m py_compile src/run_experiment.py scripts/generate_manuscript.py scripts/validate_submission_artifacts.py`
- v5 experiment run completes under thread caps.
- CSV row-count and numeric-integrity checks pass.
- PDF compiles with LaTeX/BibTeX and has at least 25 pages.
- BibTeX has zero warnings.
- Visual QA checks representative pages.
- `C:/Users/wangz/Downloads/118.pdf` exists and no numbered copies exist elsewhere.
- Public GitHub repo is updated and the pushed commit is verified.
- Root ledgers are updated only after local validation passes.
