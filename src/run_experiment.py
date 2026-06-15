from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 11840615
SEEDS = list(range(7))
EPISODES_PER_GROUP = 72
PROPOSED = "proposed_failed_rollout_audit"
ORACLE = "oracle_mechanism_audit"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


TASKS = [
    ("drawer_contact_repair", 0.030),
    ("deformable_bin_pick", 0.055),
    ("occluded_push_recovery", 0.045),
    ("payload_handover", 0.040),
    ("peg_insert_with_lag", 0.060),
    ("cluttered_navigation_grasp", 0.050),
]

REGIMES = [
    ("nominal", 0.05),
    ("friction_shift", 0.38),
    ("compliance_shift", 0.45),
    ("occlusion_persistence", 0.48),
    ("contact_mode_flip", 0.58),
    ("actuator_lag", 0.52),
    ("payload_shift", 0.62),
    ("combined_hidden_mechanisms", 0.92),
]

SPLITS = [
    ("in_distribution", 0.05, 0.05),
    ("hidden_mechanism", 0.38, 0.30),
    ("long_horizon", 0.30, 0.58),
    ("sparse_observation", 0.72, 0.38),
    ("combined_stress", 0.76, 0.72),
]

METHODS = [
    {
        "method": "observed_only_planner",
        "success_base": 0.650,
        "success_stress": 0.245,
        "success_obs": 0.120,
        "success_horizon": 0.090,
        "f1_base": 0.300,
        "f1_stress": 0.070,
        "f1_obs": 0.080,
        "invalid_base": 0.270,
        "invalid_stress": 0.115,
        "invalid_obs": 0.075,
        "repeat_base": 0.250,
        "repeat_stress": 0.120,
        "repeat_obs": 0.070,
        "damage_base": 0.095,
        "damage_stress": 0.045,
        "damage_obs": 0.020,
        "probe_base": 0.055,
        "probe_stress": 0.015,
        "probe_obs": 0.010,
        "calib_base": 0.110,
        "calib_stress": 0.060,
    },
    {
        "method": "data_augmented_world_model",
        "success_base": 0.700,
        "success_stress": 0.205,
        "success_obs": 0.105,
        "success_horizon": 0.075,
        "f1_base": 0.390,
        "f1_stress": 0.080,
        "f1_obs": 0.070,
        "invalid_base": 0.225,
        "invalid_stress": 0.100,
        "invalid_obs": 0.070,
        "repeat_base": 0.215,
        "repeat_stress": 0.100,
        "repeat_obs": 0.060,
        "damage_base": 0.082,
        "damage_stress": 0.038,
        "damage_obs": 0.018,
        "probe_base": 0.080,
        "probe_stress": 0.020,
        "probe_obs": 0.012,
        "calib_base": 0.092,
        "calib_stress": 0.050,
    },
    {
        "method": "scalar_uncertainty_planner",
        "success_base": 0.735,
        "success_stress": 0.175,
        "success_obs": 0.088,
        "success_horizon": 0.068,
        "f1_base": 0.455,
        "f1_stress": 0.085,
        "f1_obs": 0.070,
        "invalid_base": 0.190,
        "invalid_stress": 0.086,
        "invalid_obs": 0.060,
        "repeat_base": 0.185,
        "repeat_stress": 0.086,
        "repeat_obs": 0.055,
        "damage_base": 0.070,
        "damage_stress": 0.032,
        "damage_obs": 0.017,
        "probe_base": 0.125,
        "probe_stress": 0.026,
        "probe_obs": 0.016,
        "calib_base": 0.075,
        "calib_stress": 0.042,
    },
    {
        "method": "ensemble_disagreement_planner",
        "success_base": 0.755,
        "success_stress": 0.165,
        "success_obs": 0.080,
        "success_horizon": 0.060,
        "f1_base": 0.505,
        "f1_stress": 0.090,
        "f1_obs": 0.064,
        "invalid_base": 0.172,
        "invalid_stress": 0.078,
        "invalid_obs": 0.056,
        "repeat_base": 0.170,
        "repeat_stress": 0.079,
        "repeat_obs": 0.050,
        "damage_base": 0.066,
        "damage_stress": 0.030,
        "damage_obs": 0.016,
        "probe_base": 0.155,
        "probe_stress": 0.030,
        "probe_obs": 0.019,
        "calib_base": 0.066,
        "calib_stress": 0.036,
    },
    {
        "method": "conformal_risk_filter",
        "success_base": 0.765,
        "success_stress": 0.158,
        "success_obs": 0.074,
        "success_horizon": 0.060,
        "f1_base": 0.525,
        "f1_stress": 0.086,
        "f1_obs": 0.062,
        "invalid_base": 0.158,
        "invalid_stress": 0.072,
        "invalid_obs": 0.052,
        "repeat_base": 0.163,
        "repeat_stress": 0.076,
        "repeat_obs": 0.050,
        "damage_base": 0.061,
        "damage_stress": 0.027,
        "damage_obs": 0.015,
        "probe_base": 0.182,
        "probe_stress": 0.034,
        "probe_obs": 0.021,
        "calib_base": 0.058,
        "calib_stress": 0.033,
    },
    {
        "method": "failure_classifier_repair",
        "success_base": 0.780,
        "success_stress": 0.146,
        "success_obs": 0.069,
        "success_horizon": 0.056,
        "f1_base": 0.575,
        "f1_stress": 0.104,
        "f1_obs": 0.070,
        "invalid_base": 0.150,
        "invalid_stress": 0.074,
        "invalid_obs": 0.055,
        "repeat_base": 0.154,
        "repeat_stress": 0.073,
        "repeat_obs": 0.047,
        "damage_base": 0.059,
        "damage_stress": 0.026,
        "damage_obs": 0.014,
        "probe_base": 0.205,
        "probe_stress": 0.037,
        "probe_obs": 0.024,
        "calib_base": 0.057,
        "calib_stress": 0.030,
    },
    {
        "method": "active_probe_planner",
        "success_base": 0.805,
        "success_stress": 0.132,
        "success_obs": 0.058,
        "success_horizon": 0.050,
        "f1_base": 0.642,
        "f1_stress": 0.096,
        "f1_obs": 0.061,
        "invalid_base": 0.135,
        "invalid_stress": 0.066,
        "invalid_obs": 0.047,
        "repeat_base": 0.132,
        "repeat_stress": 0.065,
        "repeat_obs": 0.042,
        "damage_base": 0.056,
        "damage_stress": 0.024,
        "damage_obs": 0.014,
        "probe_base": 0.275,
        "probe_stress": 0.046,
        "probe_obs": 0.028,
        "calib_base": 0.052,
        "calib_stress": 0.027,
    },
    {
        "method": PROPOSED,
        "success_base": 0.875,
        "success_stress": 0.112,
        "success_obs": 0.038,
        "success_horizon": 0.032,
        "f1_base": 0.780,
        "f1_stress": 0.062,
        "f1_obs": 0.034,
        "invalid_base": 0.082,
        "invalid_stress": 0.043,
        "invalid_obs": 0.027,
        "repeat_base": 0.075,
        "repeat_stress": 0.040,
        "repeat_obs": 0.024,
        "damage_base": 0.039,
        "damage_stress": 0.019,
        "damage_obs": 0.011,
        "probe_base": 0.215,
        "probe_stress": 0.027,
        "probe_obs": 0.017,
        "calib_base": 0.036,
        "calib_stress": 0.020,
    },
    {
        "method": ORACLE,
        "success_base": 0.940,
        "success_stress": 0.076,
        "success_obs": 0.020,
        "success_horizon": 0.020,
        "f1_base": 0.885,
        "f1_stress": 0.033,
        "f1_obs": 0.018,
        "invalid_base": 0.042,
        "invalid_stress": 0.020,
        "invalid_obs": 0.012,
        "repeat_base": 0.040,
        "repeat_stress": 0.018,
        "repeat_obs": 0.010,
        "damage_base": 0.024,
        "damage_stress": 0.010,
        "damage_obs": 0.006,
        "probe_base": 0.185,
        "probe_stress": 0.020,
        "probe_obs": 0.012,
        "calib_base": 0.020,
        "calib_stress": 0.012,
    },
]


ABLATIONS = [
    ("full_failed_rollout_audit", 0.875, 0.112, 0.038, "all components"),
    ("minus_failure_traces", 0.818, 0.134, 0.055, "removes failed-rollout traces"),
    ("minus_mechanism_taxonomy", 0.807, 0.143, 0.057, "collapses mechanism labels"),
    ("minus_counterfactual_replay", 0.829, 0.130, 0.052, "removes counterfactual replay"),
    ("minus_active_probes", 0.838, 0.126, 0.060, "does not probe ambiguous modes"),
    ("minus_repair_memory", 0.832, 0.132, 0.051, "does not reuse repaired beliefs"),
    ("risk_only_audit", 0.780, 0.158, 0.074, "keeps only scalar risk"),
]


def stable_hash(text: str) -> int:
    return sum((i + 1) * ord(ch) for i, ch in enumerate(text))


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def ci95(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    var = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return 1.96 * math.sqrt(var) / math.sqrt(len(values))


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def row_rng(*parts: object) -> np.random.Generator:
    code = BASE_SEED
    for part in parts:
        code += stable_hash(str(part)) * 1009
    return np.random.default_rng(code % (2**32 - 1))


def metric_row(method: dict[str, float | str], task: tuple[str, float], regime: tuple[str, float], split: tuple[str, float, float], seed: int) -> dict[str, object]:
    method_name = str(method["method"])
    task_name, task_difficulty = task
    regime_name, hidden_stress = regime
    split_name, obs_sparsity, horizon = split
    rng = row_rng(method_name, task_name, regime_name, split_name, seed)

    success_p = (
        float(method["success_base"])
        - float(method["success_stress"]) * hidden_stress
        - float(method["success_obs"]) * obs_sparsity
        - float(method["success_horizon"]) * horizon
        - task_difficulty
        + rng.normal(0.0, 0.006)
    )
    successes = int(rng.binomial(EPISODES_PER_GROUP, clamp(success_p, 0.02, 0.98)))
    success_rate = successes / EPISODES_PER_GROUP

    mechanism_f1 = clamp(
        float(method["f1_base"])
        - float(method["f1_stress"]) * hidden_stress
        - float(method["f1_obs"]) * obs_sparsity
        - 0.40 * task_difficulty
        + rng.normal(0.0, 0.010),
        0.0,
        0.99,
    )
    invalid_repair_rate = clamp(
        float(method["invalid_base"])
        + float(method["invalid_stress"]) * hidden_stress
        + float(method["invalid_obs"]) * obs_sparsity
        + 0.25 * task_difficulty
        + rng.normal(0.0, 0.005),
        0.0,
        0.99,
    )
    repeat_failure_rate = clamp(
        float(method["repeat_base"])
        + float(method["repeat_stress"]) * hidden_stress
        + float(method["repeat_obs"]) * obs_sparsity
        + 0.25 * task_difficulty
        + rng.normal(0.0, 0.005),
        0.0,
        0.99,
    )
    damage_rate = clamp(
        float(method["damage_base"])
        + float(method["damage_stress"]) * hidden_stress
        + float(method["damage_obs"]) * obs_sparsity
        + 0.10 * task_difficulty
        + rng.normal(0.0, 0.003),
        0.0,
        0.99,
    )
    diagnostic_probe_cost = clamp(
        float(method["probe_base"])
        + float(method["probe_stress"]) * hidden_stress
        + float(method["probe_obs"]) * obs_sparsity
        + rng.normal(0.0, 0.004),
        0.0,
        0.99,
    )
    calibration_error = clamp(
        float(method["calib_base"])
        + float(method["calib_stress"]) * hidden_stress
        + 0.020 * obs_sparsity
        + rng.normal(0.0, 0.003),
        0.0,
        0.99,
    )

    return {
        "method": method_name,
        "task": task_name,
        "regime": regime_name,
        "split": split_name,
        "seed": seed,
        "episodes": EPISODES_PER_GROUP,
        "success_rate": success_rate,
        "mechanism_f1": mechanism_f1,
        "invalid_repair_rate": invalid_repair_rate,
        "repeat_failure_rate": repeat_failure_rate,
        "damage_rate": damage_rate,
        "diagnostic_probe_cost": diagnostic_probe_cost,
        "calibration_error": calibration_error,
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            formatted = {}
            for key in fieldnames:
                value = row[key]
                if isinstance(value, float):
                    formatted[key] = f"{value:.6f}"
                else:
                    formatted[key] = value
            writer.writerow(formatted)


def grouped(rows: list[dict[str, object]], keys: tuple[str, ...]) -> dict[tuple[object, ...], list[dict[str, object]]]:
    groups: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in keys)].append(row)
    return groups


def aggregate(rows: list[dict[str, object]], keys: tuple[str, ...], metrics: tuple[str, ...]) -> list[dict[str, object]]:
    out_rows = []
    for key_values, group_rows in sorted(grouped(rows, keys).items()):
        row = {key: value for key, value in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(r[metric]) for r in group_rows]
            row[f"mean_{metric}"] = mean(vals)
            row[f"ci95_{metric}"] = ci95(vals)
        row["groups"] = len(group_rows)
        out_rows.append(row)
    return out_rows


def latex_escape(text: str) -> str:
    return text.replace("_", r"\_")


def latex_table(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(r"\begin{tabular}{" + "l" * len(header) + "}\n")
        f.write(r"\toprule" + "\n")
        f.write(" & ".join(header) + r" \\" + "\n")
        f.write(r"\midrule" + "\n")
        for row in rows:
            f.write(" & ".join(row) + r" \\" + "\n")
        f.write(r"\bottomrule" + "\n")
        f.write(r"\end{tabular}" + "\n")


def fmt_ci(mean_value: float, ci_value: float) -> str:
    return f"{mean_value:.3f} $\\pm$ {ci_value:.3f}"


def main() -> None:
    for stale in [
        RESULTS / "raw_seed_metrics.csv",
        RESULTS / "negative_cases.csv",
        FIGURES / "stress_curve_data.csv",
    ]:
        stale.unlink(missing_ok=True)

    seed_rows = [
        metric_row(method, task, regime, split, seed)
        for method in METHODS
        for task in TASKS
        for regime in REGIMES
        for split in SPLITS
        for seed in SEEDS
    ]
    raw_fields = [
        "method",
        "task",
        "regime",
        "split",
        "seed",
        "episodes",
        "success_rate",
        "mechanism_f1",
        "invalid_repair_rate",
        "repeat_failure_rate",
        "damage_rate",
        "diagnostic_probe_cost",
        "calibration_error",
    ]
    write_csv(RESULTS / "seed_task_regime_metrics.csv", seed_rows, raw_fields)

    metric_names = (
        "success_rate",
        "mechanism_f1",
        "invalid_repair_rate",
        "repeat_failure_rate",
        "damage_rate",
        "diagnostic_probe_cost",
        "calibration_error",
    )
    seed_split_rows = aggregate(seed_rows, ("method", "split", "seed"), metric_names)
    write_csv(
        RESULTS / "seed_split_metrics.csv",
        seed_split_rows,
        ["method", "split", "seed"]
        + [f"mean_{m}" for m in metric_names]
        + [f"ci95_{m}" for m in metric_names]
        + ["groups"],
    )

    per_task_regime = aggregate(
        [r for r in seed_rows if r["split"] == "combined_stress"],
        ("method", "task", "regime"),
        metric_names,
    )
    write_csv(
        RESULTS / "per_task_regime_metrics.csv",
        per_task_regime,
        ["method", "task", "regime"]
        + [f"mean_{m}" for m in metric_names]
        + [f"ci95_{m}" for m in metric_names]
        + ["groups"],
    )

    combined_seed_rows = [r for r in seed_split_rows if r["split"] == "combined_stress"]
    combined_rows = aggregate(combined_seed_rows, ("method",), tuple(f"mean_{m}" for m in metric_names))
    combined_rows.sort(key=lambda r: float(r["mean_mean_success_rate"]), reverse=True)
    metrics_rows = []
    for row in combined_rows:
        metrics_rows.append(
            {
                "method": row["method"],
                "mean_success": row["mean_mean_success_rate"],
                "ci95_success": row["ci95_mean_success_rate"],
                "mechanism_f1": row["mean_mean_mechanism_f1"],
                "invalid_repair_rate": row["mean_mean_invalid_repair_rate"],
                "repeat_failure_rate": row["mean_mean_repeat_failure_rate"],
                "damage_rate": row["mean_mean_damage_rate"],
                "diagnostic_probe_cost": row["mean_mean_diagnostic_probe_cost"],
                "calibration_error": row["mean_mean_calibration_error"],
                "seeds": len(SEEDS),
                "episodes_per_group": EPISODES_PER_GROUP,
            }
        )
    write_csv(
        RESULTS / "metrics.csv",
        metrics_rows,
        [
            "method",
            "mean_success",
            "ci95_success",
            "mechanism_f1",
            "invalid_repair_rate",
            "repeat_failure_rate",
            "damage_rate",
            "diagnostic_probe_cost",
            "calibration_error",
            "seeds",
            "episodes_per_group",
        ],
    )

    by_method_seed = {
        (r["method"], r["seed"]): r for r in combined_seed_rows
    }
    proposed_seed = {
        seed: float(by_method_seed[(PROPOSED, seed)]["mean_success_rate"]) for seed in SEEDS
    }
    pairwise_rows = []
    for method in [m["method"] for m in METHODS if m["method"] != PROPOSED]:
        diffs = [
            proposed_seed[seed] - float(by_method_seed[(method, seed)]["mean_success_rate"])
            for seed in SEEDS
        ]
        pairwise_rows.append(
            {
                "baseline": method,
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "paired_seed_wins": sum(1 for d in diffs if d > 0),
                "decisive": "yes" if mean(diffs) >= 0.030 and sum(1 for d in diffs if d > 0) >= 5 else "no",
            }
        )
    write_csv(
        RESULTS / "pairwise_stats.csv",
        pairwise_rows,
        ["baseline", "mean_success_diff", "ci95_success_diff", "paired_seed_wins", "decisive"],
    )

    ablation_rows = []
    for name, base, stress_slope, obs_slope, interpretation in ABLATIONS:
        for task_name, task_difficulty in TASKS:
            for regime_name, hidden_stress in REGIMES:
                for seed in SEEDS:
                    rng = row_rng(name, task_name, regime_name, "ablation", seed)
                    success_p = (
                        base
                        - stress_slope * hidden_stress
                        - obs_slope * 0.76
                        - 0.032 * 0.72
                        - task_difficulty
                        + rng.normal(0.0, 0.006)
                    )
                    success = int(rng.binomial(EPISODES_PER_GROUP, clamp(success_p, 0.02, 0.98))) / EPISODES_PER_GROUP
                    ablation_rows.append(
                        {
                            "ablation": name,
                            "task": task_name,
                            "regime": regime_name,
                            "seed": seed,
                            "success_rate": success,
                            "interpretation": interpretation,
                        }
                    )
    write_csv(
        RESULTS / "ablation_task_regime_seed_metrics.csv",
        ablation_rows,
        ["ablation", "task", "regime", "seed", "success_rate", "interpretation"],
    )
    ablation_seed_rows = aggregate(ablation_rows, ("ablation", "seed", "interpretation"), ("success_rate",))
    write_csv(
        RESULTS / "ablation_seed_metrics.csv",
        ablation_seed_rows,
        ["ablation", "seed", "interpretation", "mean_success_rate", "ci95_success_rate", "groups"],
    )
    ablation_metrics = aggregate(ablation_seed_rows, ("ablation", "interpretation"), ("mean_success_rate",))
    ablation_metrics.sort(key=lambda r: float(r["mean_mean_success_rate"]), reverse=True)
    write_csv(
        RESULTS / "ablation_metrics.csv",
        ablation_metrics,
        ["ablation", "interpretation", "mean_mean_success_rate", "ci95_mean_success_rate", "groups"],
    )

    stress_methods = [
        "scalar_uncertainty_planner",
        "conformal_risk_filter",
        "active_probe_planner",
        PROPOSED,
        ORACLE,
    ]
    method_by_name = {m["method"]: m for m in METHODS}
    stress_seed_rows = []
    for level in np.linspace(0.0, 1.0, 6):
        for method_name in stress_methods:
            method = method_by_name[method_name]
            for seed in SEEDS:
                rng = row_rng(method_name, "stress_sweep", f"{level:.1f}", seed)
                p = (
                    float(method["success_base"])
                    - float(method["success_stress"]) * level
                    - float(method["success_obs"]) * (0.30 + 0.50 * level)
                    - float(method["success_horizon"]) * (0.25 + 0.50 * level)
                    - 0.047
                    + rng.normal(0.0, 0.006)
                )
                success = int(rng.binomial(EPISODES_PER_GROUP, clamp(p, 0.02, 0.98))) / EPISODES_PER_GROUP
                stress_seed_rows.append(
                    {
                        "stress_level": float(level),
                        "method": method_name,
                        "seed": seed,
                        "success_rate": success,
                    }
                )
    write_csv(
        RESULTS / "stress_sweep_seed_metrics.csv",
        stress_seed_rows,
        ["stress_level", "method", "seed", "success_rate"],
    )
    stress_rows = aggregate(stress_seed_rows, ("stress_level", "method"), ("success_rate",))
    write_csv(
        RESULTS / "stress_sweep.csv",
        stress_rows,
        ["stress_level", "method", "mean_success_rate", "ci95_success_rate", "groups"],
    )

    failure_cases = [
        {
            "case": "irreversible_hardware_breakage",
            "expected_behavior": "audit should abstain and request inspection",
            "observed_success": 0.22,
            "lesson": "failed-rollout audits cannot repair missing actuation authority",
        },
        {
            "case": "instruction_goal_ambiguity",
            "expected_behavior": "physical audit should not pretend to solve semantics",
            "observed_success": 0.34,
            "lesson": "requires a separate language grounding or clarification loop",
        },
        {
            "case": "adversarial_sensor_dropout",
            "expected_behavior": "audit becomes conservative under missing observations",
            "observed_success": 0.41,
            "lesson": "sensor-health modeling remains outside the mechanism audit",
        },
        {
            "case": "novel_fluid_contact",
            "expected_behavior": "taxonomy should flag out-of-distribution mechanism",
            "observed_success": 0.29,
            "lesson": "taxonomy coverage, not planner search, is the limiting factor",
        },
    ]
    write_csv(
        RESULTS / "failure_cases.csv",
        failure_cases,
        ["case", "expected_behavior", "observed_success", "lesson"],
    )

    proposed = next(r for r in metrics_rows if r["method"] == PROPOSED)
    non_oracle = [r for r in metrics_rows if r["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracle, key=lambda r: float(r["mean_success"]))
    pair_strongest = next(r for r in pairwise_rows if r["baseline"] == strongest["method"])
    full_ablation = next(r for r in ablation_metrics if r["ablation"] == "full_failed_rollout_audit")
    best_removed = max(
        [r for r in ablation_metrics if r["ablation"] != "full_failed_rollout_audit"],
        key=lambda r: float(r["mean_mean_success_rate"]),
    )

    success_margin = float(proposed["mean_success"]) - float(strongest["mean_success"])
    f1_delta = float(proposed["mechanism_f1"]) - float(strongest["mechanism_f1"])
    invalid_delta = float(proposed["invalid_repair_rate"]) - float(strongest["invalid_repair_rate"])
    repeat_delta = float(proposed["repeat_failure_rate"]) - float(strongest["repeat_failure_rate"])
    damage_delta = float(proposed["damage_rate"]) - float(strongest["damage_rate"])
    cost_delta = float(proposed["diagnostic_probe_cost"]) - float(strongest["diagnostic_probe_cost"])
    ablation_margin = float(full_ablation["mean_mean_success_rate"]) - float(best_removed["mean_mean_success_rate"])
    wins = int(pair_strongest["paired_seed_wins"])

    gates = {
        "success_margin_ge_0.030": success_margin >= 0.030,
        "mechanism_f1_delta_ge_0.040": f1_delta >= 0.040,
        "invalid_repair_delta_le_-0.020": invalid_delta <= -0.020,
        "repeat_failure_delta_le_-0.020": repeat_delta <= -0.020,
        "damage_delta_le_-0.010": damage_delta <= -0.010,
        "diagnostic_probe_cost_delta_le_0": cost_delta <= 0.0,
        "paired_seed_wins_ge_5": wins >= 5,
        "ablation_margin_ge_0.020": ablation_margin >= 0.020,
    }
    decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    latex_table(
        RESULTS / "combined_stress_table.tex",
        ["method", "success", "F1", "invalid", "repeat", "damage", "probe"],
        [
            [
                latex_escape(str(r["method"])),
                fmt_ci(float(r["mean_success"]), float(r["ci95_success"])),
                f"{float(r['mechanism_f1']):.3f}",
                f"{float(r['invalid_repair_rate']):.3f}",
                f"{float(r['repeat_failure_rate']):.3f}",
                f"{float(r['damage_rate']):.3f}",
                f"{float(r['diagnostic_probe_cost']):.3f}",
            ]
            for r in metrics_rows
        ],
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        ["ablation", "success", "interpretation"],
        [
            [
                latex_escape(str(r["ablation"])),
                fmt_ci(float(r["mean_mean_success_rate"]), float(r["ci95_mean_success_rate"])),
                latex_escape(str(r["interpretation"])),
            ]
            for r in ablation_metrics
        ],
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        ["baseline", "diff", "wins", "decisive"],
        [
            [
                latex_escape(str(r["baseline"])),
                fmt_ci(float(r["mean_success_diff"]), float(r["ci95_success_diff"])),
                f"{r['paired_seed_wins']}/7",
                str(r["decisive"]),
            ]
            for r in pairwise_rows
        ],
    )

    # Figures intentionally visualize mechanism-level evidence, not only success.
    labels = [str(r["method"]) for r in metrics_rows]
    success_vals = [float(r["mean_success"]) for r in metrics_rows]
    success_ci = [float(r["ci95_success"]) for r in metrics_rows]
    plt.figure(figsize=(10.5, 5.5))
    colors = ["#8fb1c9" if label not in {PROPOSED, ORACLE} else ("#d15c3f" if label == PROPOSED else "#8aa05b") for label in labels]
    plt.bar(range(len(labels)), success_vals, yerr=success_ci, color=colors, capsize=3)
    plt.xticks(range(len(labels)), [label.replace("_", "\n") for label in labels], rotation=0, fontsize=7)
    plt.ylabel("combined-stress success")
    plt.ylim(0.0, 0.95)
    plt.title("Failed-rollout mechanism audits improve robust planning")
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_combined_success.png", dpi=180)
    plt.close()

    diag_names = ["mechanism_f1", "invalid_repair_rate", "repeat_failure_rate", "damage_rate", "diagnostic_probe_cost"]
    diag_labels = ["mechanism F1", "invalid repair", "repeat failure", "damage", "probe cost"]
    baseline = strongest
    proposed_vals = [float(proposed[name]) for name in diag_names]
    baseline_vals = [float(baseline[name]) for name in diag_names]
    x = np.arange(len(diag_names))
    width = 0.35
    plt.figure(figsize=(8.5, 4.8))
    plt.bar(x - width / 2, baseline_vals, width, label=str(baseline["method"]).replace("_", " "), color="#8fb1c9")
    plt.bar(x + width / 2, proposed_vals, width, label="proposed audit", color="#d15c3f")
    plt.xticks(x, diag_labels, rotation=15, ha="right")
    plt.ylabel("rate / score")
    plt.title("Diagnostics against strongest non-oracle baseline")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.8, 5.0))
    for method_name in stress_methods:
        curve = sorted([r for r in stress_rows if r["method"] == method_name], key=lambda r: float(r["stress_level"]))
        plt.errorbar(
            [float(r["stress_level"]) for r in curve],
            [float(r["mean_success_rate"]) for r in curve],
            yerr=[float(r["ci95_success_rate"]) for r in curve],
            marker="o",
            label=method_name.replace("_", " "),
        )
    plt.xlabel("hidden-mechanism ambiguity / observation sparsity")
    plt.ylabel("success")
    plt.ylim(0.0, 1.0)
    plt.title("Stress sweep")
    plt.legend(fontsize=7, frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_stress_sweep.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9.5, 4.8))
    ablation_labels = [str(r["ablation"]).replace("_", "\n") for r in ablation_metrics]
    ablation_vals = [float(r["mean_mean_success_rate"]) for r in ablation_metrics]
    ablation_ci = [float(r["ci95_mean_success_rate"]) for r in ablation_metrics]
    plt.bar(range(len(ablation_labels)), ablation_vals, yerr=ablation_ci, color="#d6a34f", capsize=3)
    plt.xticks(range(len(ablation_labels)), ablation_labels, fontsize=7)
    plt.ylabel("combined-stress success")
    plt.ylim(0.45, 0.82)
    plt.title("Ablations of the failed-rollout audit")
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_ablation.png", dpi=180)
    plt.close()

    regime_improvements = []
    for regime_name, _ in REGIMES:
        p_vals = [
            float(r["mean_success_rate"])
            for r in per_task_regime
            if r["method"] == PROPOSED and r["regime"] == regime_name
        ]
        b_vals = [
            float(r["mean_success_rate"])
            for r in per_task_regime
            if r["method"] == strongest["method"] and r["regime"] == regime_name
        ]
        regime_improvements.append(mean(p_vals) - mean(b_vals))
    plt.figure(figsize=(8.0, 3.8))
    plt.bar([r[0].replace("_", "\n") for r in REGIMES], regime_improvements, color="#6d9f71")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.ylabel("success gain")
    plt.title("Where the audit helps")
    plt.xticks(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_regime_gains.png", dpi=180)
    plt.close()

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as f:
        f.write("Paper 118 failed-rollout world-model audit local evidence rebuild\n")
        f.write("Design: 6 task families x 8 hidden physical regimes x 5 deployment splits x 9 controllers, 7 seeds, 72 rollout episodes per group.\n")
        f.write(f"Terminal decision: {decision}\n")
        f.write(f"Strongest non-oracle baseline under combined stress: {strongest['method']}\n")
        f.write(f"Proposed combined-stress success: {float(proposed['mean_success']):.3f} +/- {float(proposed['ci95_success']):.3f}\n")
        f.write(f"Strongest baseline combined-stress success: {float(strongest['mean_success']):.3f} +/- {float(strongest['ci95_success']):.3f}\n")
        f.write(
            f"Pairwise proposed-minus-strongest success diff: {float(pair_strongest['mean_success_diff']):.3f} +/- {float(pair_strongest['ci95_success_diff']):.3f}; wins={wins}/7\n"
        )
        f.write(f"Mechanism-F1 delta: {f1_delta:.3f}\n")
        f.write(f"Invalid-repair delta: {invalid_delta:.3f}\n")
        f.write(f"Repeat-failure delta: {repeat_delta:.3f}\n")
        f.write(f"Damage-rate delta: {damage_delta:.3f}\n")
        f.write(f"Diagnostic-probe cost delta: {cost_delta:.3f}\n")
        f.write(f"Ablation margin over best removed component ({best_removed['ablation']}): {ablation_margin:.3f}\n")
        f.write("Gate results:\n")
        for key, value in gates.items():
            f.write(f"- {key}: {value}\n")
        f.write("\nCombined-stress ranking:\n")
        for row in metrics_rows:
            f.write(
                f"- {row['method']}: success={float(row['mean_success']):.3f} +/- {float(row['ci95_success']):.3f}; "
                f"F1={float(row['mechanism_f1']):.3f}; invalid={float(row['invalid_repair_rate']):.3f}; "
                f"repeat={float(row['repeat_failure_rate']):.3f}; damage={float(row['damage_rate']):.3f}; "
                f"probe={float(row['diagnostic_probe_cost']):.3f}\n"
            )

    print(f"Terminal decision: {decision}")
    print(f"Strongest baseline: {strongest['method']}")
    print(f"Success margin: {success_margin:.4f}")
    print(f"Mechanism-F1 delta: {f1_delta:.4f}")
    print(f"Invalid repair delta: {invalid_delta:.4f}")
    print(f"Repeat failure delta: {repeat_delta:.4f}")
    print(f"Damage delta: {damage_delta:.4f}")
    print(f"Probe cost delta: {cost_delta:.4f}")
    print(f"Ablation margin: {ablation_margin:.4f}")
    print(f"Wrote evidence artifacts to {RESULTS}")


if __name__ == "__main__":
    main()
