# 118 World-Model Audits From Failed Rollouts

Expanded-standard version: v5

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

Paper 118 has been rebuilt from the v4.1 4-page scaffold into a 28-page v5 manuscript. The new method, `counterfactual_mechanism_audit_v5`, converts failed robot rollouts into a typed mechanism posterior and then chooses repair, diagnostic probe, abstention, or conservative fallback. The package is still not ICLR-main ready because it lacks real robot or accepted high-fidelity validation.

## Evidence Snapshot

- Canonical PDF: `C:/Users/wangz/Downloads/118.pdf`
- PDF pages: 28
- PDF SHA256: `2AC788263369C553819D52E8E6715D108901635A944E4783E39044A506C58C11`
- PDF size: `728828` bytes
- Artifact rule: numbered PDF in Downloads only; no Desktop copy.
- Strongest non-oracle baseline: `proposed_failed_rollout_audit_v4_1`
- Proposed hard success: `0.80583`
- Strongest baseline hard success: `0.70615`
- Proposed hard utility: `0.68463`
- Strongest baseline hard utility: `0.42095`
- Mechanism-F1 delta: `+0.08835`
- Invalid-repair delta: `-0.04046`
- Repeat-failure delta: `-0.03822`
- Damage-rate delta: `-0.01269`
- Diagnostic-probe cost delta: `-0.03908`
- Calibration-error delta: `-0.01950`
- Budget-violation delta: `-0.05457`
- Paired hard utility wins: `10/10`
- Best removed-component ablation: `minus_active_probe_value`
- Ablation success margin: `0.02135`
- Ablation utility margin: `0.04107`
- Max-stress success margin: `0.14401`
- Max-stress utility margin: `0.32111`
- Strict fixed-budget coverage: `0.62552`
- Strict fixed-budget breach: `0.00000`
- Strict fixed-budget gated success: `0.78912`

## Generated Evidence

- `230,400` main rollout cells
- `2,880` main group rows
- `600` seed-metric rows
- `12` aggregate method rows
- `120` hard seed rows
- `12` hard aggregate rows
- `11` hard pairwise rows
- `38,400` ablation cells
- `161,280` stress cells
- `107,520` fixed-budget cells
- `24` failure cases

## Reproduce

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py scripts\generate_manuscript.py scripts\validate_submission_artifacts.py
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item paper\main.pdf C:\Users\wangz\Downloads\118.pdf -Force
python scripts\validate_submission_artifacts.py
```

## Decision Boundary

Local gates pass, so the paper is `STRONG_REVISE`. ICLR-main readiness remains `no` because the package still has no real robot rollouts, no accepted high-fidelity robot world-model simulation, no released world-model or policy checkpoint, no calibrated contact-force/camera/state logs, no hardware rollout videos, no independent baseline implementations, and no complete manual related-work synthesis.
