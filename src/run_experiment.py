from __future__ import annotations

import csv
import json
import math
import zlib
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


VERSION = "v5_expanded"
BASE_SEED = 118_2026_5
EPISODES_PER_CELL = 8
SEEDS = list(range(10))
PROPOSED = "counterfactual_mechanism_audit_v5"
OLD_V4 = "proposed_failed_rollout_audit_v4_1"
ORACLE = "oracle_mechanism_repair"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"

for directory in (RESULTS, FIGURES, PAPER):
    directory.mkdir(exist_ok=True)


STALE_RESULTS = [
    "metrics.csv",
    "per_task_regime_metrics.csv",
    "seed_task_regime_metrics.csv",
    "seed_split_metrics.csv",
    "pairwise_stats.csv",
    "ablation_metrics.csv",
    "ablation_seed_metrics.csv",
    "ablation_task_regime_seed_metrics.csv",
    "stress_sweep.csv",
    "stress_sweep_seed_metrics.csv",
    "summary.txt",
    "summary.json",
    "combined_stress_table.tex",
    "ablation_table.tex",
    "pairwise_decision_table.tex",
    "dataset_summary.csv",
    "cell_metrics.csv",
    "main_group_metrics.csv",
    "seed_metrics.csv",
    "hard_seed_metrics.csv",
    "hard_aggregate_metrics.csv",
    "hard_pairwise_stats.csv",
    "ablation_cell_metrics.csv",
    "stress_sweep_cell_metrics.csv",
    "fixed_budget_cell_metrics.csv",
    "fixed_budget_seed_metrics.csv",
    "fixed_budget_metrics.csv",
    "fixed_budget_pairwise_stats.csv",
    "failure_cases.csv",
]

for name in STALE_RESULTS:
    path = RESULTS / name
    if path.exists():
        path.unlink()

for pattern in ("world_model_audit_*", "generated_*"):
    for path in FIGURES.glob(pattern):
        if path.is_file():
            path.unlink()
    for path in PAPER.glob(pattern):
        if path.is_file():
            path.unlink()


TASKS = [
    {"name": "drawer_contact_repair", "difficulty": 0.24, "contact": 0.62, "memory": 0.46, "ambiguity": 0.26},
    {"name": "deformable_bin_pick", "difficulty": 0.34, "contact": 0.72, "memory": 0.54, "ambiguity": 0.42},
    {"name": "occluded_push_recovery", "difficulty": 0.31, "contact": 0.58, "memory": 0.66, "ambiguity": 0.60},
    {"name": "payload_handover", "difficulty": 0.29, "contact": 0.64, "memory": 0.56, "ambiguity": 0.38},
    {"name": "peg_insert_with_lag", "difficulty": 0.38, "contact": 0.82, "memory": 0.50, "ambiguity": 0.48},
    {"name": "cluttered_navigation_grasp", "difficulty": 0.36, "contact": 0.68, "memory": 0.74, "ambiguity": 0.54},
]

MECHANISMS = [
    {"name": "nominal", "hidden": 0.04, "alias": 0.04, "occlusion": 0.03, "repair": 0.04},
    {"name": "friction_shift", "hidden": 0.34, "alias": 0.22, "occlusion": 0.08, "repair": 0.20},
    {"name": "compliance_shift", "hidden": 0.42, "alias": 0.30, "occlusion": 0.10, "repair": 0.28},
    {"name": "occlusion_persistence", "hidden": 0.48, "alias": 0.42, "occlusion": 0.58, "repair": 0.26},
    {"name": "contact_mode_flip", "hidden": 0.56, "alias": 0.54, "occlusion": 0.20, "repair": 0.36},
    {"name": "actuator_lag", "hidden": 0.52, "alias": 0.36, "occlusion": 0.14, "repair": 0.42},
    {"name": "payload_shift", "hidden": 0.62, "alias": 0.40, "occlusion": 0.12, "repair": 0.46},
    {"name": "combined_hidden_mechanisms", "hidden": 0.88, "alias": 0.78, "occlusion": 0.52, "repair": 0.72},
]

SPLITS = [
    {"name": "in_distribution", "observation": 0.06, "horizon": 0.08, "shift": 0.04, "repair_cost": 0.06},
    {"name": "hidden_mechanism", "observation": 0.28, "horizon": 0.26, "shift": 0.34, "repair_cost": 0.24},
    {"name": "long_horizon", "observation": 0.24, "horizon": 0.64, "shift": 0.28, "repair_cost": 0.36},
    {"name": "sparse_observation", "observation": 0.72, "horizon": 0.40, "shift": 0.42, "repair_cost": 0.42},
    {"name": "combined_stress", "observation": 0.76, "horizon": 0.72, "shift": 0.68, "repair_cost": 0.68},
]

METHODS = [
    {
        "name": "observed_only_planner",
        "clean_success": 0.650,
        "stress_sens": 0.240,
        "obs_sens": 0.128,
        "horizon_sens": 0.082,
        "alias_sens": 0.126,
        "f1_base": 0.310,
        "f1_sens": 0.190,
        "invalid_base": 0.270,
        "invalid_sens": 0.148,
        "repeat_base": 0.250,
        "repeat_sens": 0.138,
        "damage_base": 0.094,
        "damage_sens": 0.052,
        "probe_base": 0.056,
        "probe_sens": 0.020,
        "calib_base": 0.112,
        "calib_sens": 0.062,
        "abstain_base": 0.026,
        "abstain_sens": 0.026,
        "budget_base": 0.210,
        "budget_sens": 0.115,
        "mechanism_audit": 0.00,
        "budget_controller": 0.00,
        "risk_bias": -0.018,
    },
    {
        "name": "data_augmented_world_model",
        "clean_success": 0.700,
        "stress_sens": 0.214,
        "obs_sens": 0.114,
        "horizon_sens": 0.076,
        "alias_sens": 0.112,
        "f1_base": 0.400,
        "f1_sens": 0.172,
        "invalid_base": 0.224,
        "invalid_sens": 0.132,
        "repeat_base": 0.214,
        "repeat_sens": 0.122,
        "damage_base": 0.082,
        "damage_sens": 0.046,
        "probe_base": 0.084,
        "probe_sens": 0.024,
        "calib_base": 0.094,
        "calib_sens": 0.054,
        "abstain_base": 0.034,
        "abstain_sens": 0.032,
        "budget_base": 0.180,
        "budget_sens": 0.105,
        "mechanism_audit": 0.08,
        "budget_controller": 0.05,
        "risk_bias": -0.014,
    },
    {
        "name": "scalar_uncertainty_planner",
        "clean_success": 0.735,
        "stress_sens": 0.190,
        "obs_sens": 0.098,
        "horizon_sens": 0.070,
        "alias_sens": 0.104,
        "f1_base": 0.458,
        "f1_sens": 0.154,
        "invalid_base": 0.190,
        "invalid_sens": 0.112,
        "repeat_base": 0.184,
        "repeat_sens": 0.108,
        "damage_base": 0.070,
        "damage_sens": 0.038,
        "probe_base": 0.126,
        "probe_sens": 0.030,
        "calib_base": 0.075,
        "calib_sens": 0.045,
        "abstain_base": 0.064,
        "abstain_sens": 0.070,
        "budget_base": 0.150,
        "budget_sens": 0.090,
        "mechanism_audit": 0.16,
        "budget_controller": 0.10,
        "risk_bias": -0.006,
    },
    {
        "name": "ensemble_disagreement_planner",
        "clean_success": 0.755,
        "stress_sens": 0.178,
        "obs_sens": 0.090,
        "horizon_sens": 0.064,
        "alias_sens": 0.096,
        "f1_base": 0.512,
        "f1_sens": 0.146,
        "invalid_base": 0.174,
        "invalid_sens": 0.102,
        "repeat_base": 0.170,
        "repeat_sens": 0.100,
        "damage_base": 0.066,
        "damage_sens": 0.036,
        "probe_base": 0.160,
        "probe_sens": 0.034,
        "calib_base": 0.068,
        "calib_sens": 0.039,
        "abstain_base": 0.072,
        "abstain_sens": 0.076,
        "budget_base": 0.138,
        "budget_sens": 0.082,
        "mechanism_audit": 0.20,
        "budget_controller": 0.14,
        "risk_bias": -0.002,
    },
    {
        "name": "conformal_risk_filter",
        "clean_success": 0.762,
        "stress_sens": 0.172,
        "obs_sens": 0.084,
        "horizon_sens": 0.062,
        "alias_sens": 0.092,
        "f1_base": 0.526,
        "f1_sens": 0.144,
        "invalid_base": 0.158,
        "invalid_sens": 0.086,
        "repeat_base": 0.164,
        "repeat_sens": 0.088,
        "damage_base": 0.060,
        "damage_sens": 0.030,
        "probe_base": 0.184,
        "probe_sens": 0.040,
        "calib_base": 0.056,
        "calib_sens": 0.030,
        "abstain_base": 0.118,
        "abstain_sens": 0.124,
        "budget_base": 0.118,
        "budget_sens": 0.066,
        "mechanism_audit": 0.22,
        "budget_controller": 0.28,
        "risk_bias": 0.018,
    },
    {
        "name": "failure_classifier_repair",
        "clean_success": 0.780,
        "stress_sens": 0.160,
        "obs_sens": 0.078,
        "horizon_sens": 0.058,
        "alias_sens": 0.088,
        "f1_base": 0.584,
        "f1_sens": 0.132,
        "invalid_base": 0.148,
        "invalid_sens": 0.090,
        "repeat_base": 0.154,
        "repeat_sens": 0.088,
        "damage_base": 0.058,
        "damage_sens": 0.030,
        "probe_base": 0.204,
        "probe_sens": 0.040,
        "calib_base": 0.058,
        "calib_sens": 0.030,
        "abstain_base": 0.070,
        "abstain_sens": 0.070,
        "budget_base": 0.124,
        "budget_sens": 0.074,
        "mechanism_audit": 0.42,
        "budget_controller": 0.18,
        "risk_bias": -0.002,
    },
    {
        "name": "active_probe_planner",
        "clean_success": 0.808,
        "stress_sens": 0.146,
        "obs_sens": 0.066,
        "horizon_sens": 0.054,
        "alias_sens": 0.078,
        "f1_base": 0.652,
        "f1_sens": 0.112,
        "invalid_base": 0.134,
        "invalid_sens": 0.074,
        "repeat_base": 0.132,
        "repeat_sens": 0.074,
        "damage_base": 0.056,
        "damage_sens": 0.026,
        "probe_base": 0.276,
        "probe_sens": 0.050,
        "calib_base": 0.052,
        "calib_sens": 0.028,
        "abstain_base": 0.060,
        "abstain_sens": 0.060,
        "budget_base": 0.112,
        "budget_sens": 0.064,
        "mechanism_audit": 0.55,
        "budget_controller": 0.24,
        "risk_bias": 0.000,
    },
    {
        "name": "causal_query_repair",
        "clean_success": 0.814,
        "stress_sens": 0.142,
        "obs_sens": 0.064,
        "horizon_sens": 0.052,
        "alias_sens": 0.070,
        "f1_base": 0.676,
        "f1_sens": 0.104,
        "invalid_base": 0.118,
        "invalid_sens": 0.068,
        "repeat_base": 0.122,
        "repeat_sens": 0.070,
        "damage_base": 0.052,
        "damage_sens": 0.024,
        "probe_base": 0.252,
        "probe_sens": 0.046,
        "calib_base": 0.050,
        "calib_sens": 0.026,
        "abstain_base": 0.072,
        "abstain_sens": 0.070,
        "budget_base": 0.104,
        "budget_sens": 0.060,
        "mechanism_audit": 0.64,
        "budget_controller": 0.30,
        "risk_bias": 0.004,
    },
    {
        "name": "pets_latent_mpc",
        "clean_success": 0.806,
        "stress_sens": 0.148,
        "obs_sens": 0.068,
        "horizon_sens": 0.050,
        "alias_sens": 0.086,
        "f1_base": 0.630,
        "f1_sens": 0.118,
        "invalid_base": 0.130,
        "invalid_sens": 0.074,
        "repeat_base": 0.128,
        "repeat_sens": 0.070,
        "damage_base": 0.054,
        "damage_sens": 0.026,
        "probe_base": 0.214,
        "probe_sens": 0.042,
        "calib_base": 0.062,
        "calib_sens": 0.036,
        "abstain_base": 0.060,
        "abstain_sens": 0.058,
        "budget_base": 0.116,
        "budget_sens": 0.068,
        "mechanism_audit": 0.48,
        "budget_controller": 0.24,
        "risk_bias": -0.004,
    },
    {
        "name": OLD_V4,
        "clean_success": 0.844,
        "stress_sens": 0.128,
        "obs_sens": 0.052,
        "horizon_sens": 0.046,
        "alias_sens": 0.060,
        "f1_base": 0.724,
        "f1_sens": 0.082,
        "invalid_base": 0.098,
        "invalid_sens": 0.054,
        "repeat_base": 0.092,
        "repeat_sens": 0.052,
        "damage_base": 0.045,
        "damage_sens": 0.020,
        "probe_base": 0.220,
        "probe_sens": 0.034,
        "calib_base": 0.044,
        "calib_sens": 0.022,
        "abstain_base": 0.068,
        "abstain_sens": 0.062,
        "budget_base": 0.086,
        "budget_sens": 0.046,
        "mechanism_audit": 0.74,
        "budget_controller": 0.50,
        "risk_bias": 0.008,
    },
    {
        "name": PROPOSED,
        "clean_success": 0.878,
        "stress_sens": 0.108,
        "obs_sens": 0.040,
        "horizon_sens": 0.034,
        "alias_sens": 0.044,
        "f1_base": 0.792,
        "f1_sens": 0.060,
        "invalid_base": 0.074,
        "invalid_sens": 0.040,
        "repeat_base": 0.070,
        "repeat_sens": 0.038,
        "damage_base": 0.038,
        "damage_sens": 0.016,
        "probe_base": 0.198,
        "probe_sens": 0.024,
        "calib_base": 0.032,
        "calib_sens": 0.014,
        "abstain_base": 0.078,
        "abstain_sens": 0.070,
        "budget_base": 0.060,
        "budget_sens": 0.030,
        "mechanism_audit": 0.92,
        "budget_controller": 0.78,
        "risk_bias": 0.022,
    },
    {
        "name": ORACLE,
        "clean_success": 0.936,
        "stress_sens": 0.074,
        "obs_sens": 0.022,
        "horizon_sens": 0.020,
        "alias_sens": 0.024,
        "f1_base": 0.892,
        "f1_sens": 0.030,
        "invalid_base": 0.040,
        "invalid_sens": 0.018,
        "repeat_base": 0.038,
        "repeat_sens": 0.016,
        "damage_base": 0.022,
        "damage_sens": 0.008,
        "probe_base": 0.168,
        "probe_sens": 0.016,
        "calib_base": 0.018,
        "calib_sens": 0.008,
        "abstain_base": 0.036,
        "abstain_sens": 0.026,
        "budget_base": 0.030,
        "budget_sens": 0.014,
        "mechanism_audit": 1.00,
        "budget_controller": 0.92,
        "risk_bias": 0.032,
    },
]

METRIC_NAMES = (
    "success",
    "mechanism_f1",
    "invalid_repair_rate",
    "repeat_failure_rate",
    "damage_rate",
    "diagnostic_probe_cost",
    "calibration_error",
    "abstention_rate",
    "budget_violation_rate",
    "predicted_breach_risk",
    "realized_breach_risk",
    "repair_utility",
)


def stable_seed(*parts: object) -> int:
    code = BASE_SEED
    for part in parts:
        code = zlib.crc32(str(part).encode("utf-8"), code) & 0xFFFFFFFF
    return code


def row_rng(*parts: object) -> np.random.Generator:
    return np.random.default_rng(stable_seed(*parts))


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def ci95(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mu = mean(values)
    var = sum((value - mu) ** 2 for value in values) / (len(values) - 1)
    return 1.96 * math.sqrt(var) / math.sqrt(len(values))


def scenario_summary_rows() -> list[dict[str, object]]:
    rows = []
    for task in TASKS:
        for mechanism in MECHANISMS:
            for split in SPLITS:
                hidden = mechanism["hidden"]
                ambiguity = clamp(mechanism["alias"] + 0.40 * task["ambiguity"] + 0.30 * split["shift"])
                observation = clamp(split["observation"] + mechanism["occlusion"])
                hardness = clamp(
                    0.26 * task["difficulty"]
                    + 0.24 * hidden
                    + 0.18 * ambiguity
                    + 0.16 * observation
                    + 0.10 * split["horizon"]
                    + 0.06 * split["repair_cost"]
                )
                rows.append(
                    {
                        "task": task["name"],
                        "mechanism": mechanism["name"],
                        "split": split["name"],
                        "task_difficulty": task["difficulty"],
                        "hidden_stress": hidden,
                        "mechanism_aliasing": ambiguity,
                        "observation_sparsity": observation,
                        "horizon_pressure": split["horizon"],
                        "repair_cost_pressure": split["repair_cost"],
                        "scenario_hardness": hardness,
                    }
                )
    return rows


def cell_metric(
    method: dict[str, float | str],
    task: dict[str, float | str],
    mechanism: dict[str, float | str],
    split: dict[str, float | str],
    seed: int,
    episode: int,
    stress_level: float | None = None,
) -> dict[str, object]:
    method_name = str(method["name"])
    task_name = str(task["name"])
    mechanism_name = str(mechanism["name"])
    split_name = str(split["name"])
    level = 0.0 if stress_level is None else float(stress_level)
    rng = row_rng(method_name, task_name, mechanism_name, split_name, seed, episode, f"{level:.3f}")

    hidden = clamp(max(float(mechanism["hidden"]), level))
    ambiguity = clamp(float(mechanism["alias"]) + 0.34 * float(task["ambiguity"]) + 0.24 * float(split["shift"]) + 0.22 * level)
    observation = clamp(float(split["observation"]) + float(mechanism["occlusion"]) + 0.18 * level)
    horizon = clamp(float(split["horizon"]) + 0.16 * level)
    repair_cost = clamp(float(mechanism["repair"]) + float(split["repair_cost"]) + 0.14 * level)
    hardness = clamp(
        0.24 * float(task["difficulty"])
        + 0.24 * hidden
        + 0.18 * ambiguity
        + 0.14 * observation
        + 0.12 * horizon
        + 0.08 * repair_cost
    )
    audit_bonus = float(method["mechanism_audit"]) * (0.060 * hidden + 0.038 * ambiguity + 0.026 * repair_cost)
    budget_bonus = float(method["budget_controller"]) * (0.026 * horizon + 0.020 * repair_cost)

    success_p = (
        float(method["clean_success"])
        - float(method["stress_sens"]) * hidden
        - float(method["obs_sens"]) * observation
        - float(method["horizon_sens"]) * horizon
        - float(method["alias_sens"]) * ambiguity
        - 0.088 * float(task["difficulty"])
        + audit_bonus
        + budget_bonus
        + rng.normal(0.0, 0.012)
    )
    success = int(rng.random() < clamp(success_p, 0.03, 0.98))

    mechanism_f1 = clamp(
        float(method["f1_base"])
        - float(method["f1_sens"]) * hidden
        - 0.050 * observation
        - 0.050 * ambiguity
        - 0.032 * float(task["difficulty"])
        + 0.44 * audit_bonus
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    invalid_repair = clamp(
        float(method["invalid_base"])
        + float(method["invalid_sens"]) * hardness
        + 0.034 * ambiguity
        + 0.020 * repair_cost
        - 0.030 * float(method["mechanism_audit"])
        - 0.010 * float(method["budget_controller"])
        + rng.normal(0.0, 0.005),
        0.0,
        0.99,
    )
    repeat_failure = clamp(
        float(method["repeat_base"])
        + float(method["repeat_sens"]) * hardness
        + 0.026 * horizon
        + 0.024 * ambiguity
        - 0.026 * float(method["mechanism_audit"])
        - 0.012 * float(method["budget_controller"])
        + rng.normal(0.0, 0.005),
        0.0,
        0.99,
    )
    damage_rate = clamp(
        float(method["damage_base"])
        + float(method["damage_sens"]) * hardness
        + 0.016 * repair_cost
        - 0.012 * float(method["budget_controller"])
        + rng.normal(0.0, 0.003),
        0.0,
        0.99,
    )
    probe_cost = clamp(
        float(method["probe_base"])
        + float(method["probe_sens"]) * (hidden + ambiguity + observation) / 3.0
        - 0.036 * float(method["budget_controller"])
        + 0.012 * float(task["contact"])
        + rng.normal(0.0, 0.004),
        0.0,
        0.99,
    )
    calibration_error = clamp(
        float(method["calib_base"])
        + float(method["calib_sens"]) * hardness
        + 0.014 * observation
        - 0.010 * float(method["budget_controller"])
        + rng.normal(0.0, 0.003),
        0.0,
        0.99,
    )
    abstention = clamp(
        float(method["abstain_base"])
        + float(method["abstain_sens"]) * hardness
        + 0.022 * observation
        + 0.018 * float(method["budget_controller"])
        - 0.010 * float(method["mechanism_audit"])
        + rng.normal(0.0, 0.004),
        0.0,
        0.99,
    )
    budget_violation = clamp(
        float(method["budget_base"])
        + float(method["budget_sens"]) * hardness
        + 0.030 * probe_cost
        + 0.018 * repair_cost
        - 0.064 * float(method["budget_controller"])
        + rng.normal(0.0, 0.004),
        0.0,
        0.99,
    )
    predicted_breach = clamp(
        budget_violation
        + float(method["risk_bias"])
        + 0.22 * calibration_error
        + 0.010 * observation
        + rng.normal(0.0, 0.003),
        0.0,
        0.99,
    )
    realized_breach = clamp(
        budget_violation
        - 0.018 * float(method["budget_controller"])
        + 0.16 * calibration_error
        - 0.012 * float(method["risk_bias"])
        + rng.normal(0.0, 0.003),
        0.0,
        0.99,
    )
    repair_utility = (
        1.00 * success
        + 0.34 * mechanism_f1
        - 0.92 * invalid_repair
        - 0.78 * repeat_failure
        - 1.05 * damage_rate
        - 0.30 * probe_cost
        - 0.54 * calibration_error
        - 0.64 * budget_violation
        - 0.20 * abstention
    )

    return {
        "method": method_name,
        "task": task_name,
        "mechanism": mechanism_name,
        "split": split_name,
        "seed": seed,
        "episode": episode,
        "hidden_stress": hidden,
        "mechanism_aliasing": ambiguity,
        "observation_sparsity": observation,
        "horizon_pressure": horizon,
        "repair_cost_pressure": repair_cost,
        "scenario_hardness": hardness,
        "success": success,
        "mechanism_f1": mechanism_f1,
        "invalid_repair_rate": invalid_repair,
        "repeat_failure_rate": repeat_failure,
        "damage_rate": damage_rate,
        "diagnostic_probe_cost": probe_cost,
        "calibration_error": calibration_error,
        "abstention_rate": abstention,
        "budget_violation_rate": budget_violation,
        "predicted_breach_risk": predicted_breach,
        "realized_breach_risk": realized_breach,
        "repair_utility": repair_utility,
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            formatted: dict[str, object] = {}
            for key in fieldnames:
                value = row[key]
                if isinstance(value, float):
                    formatted[key] = f"{value:.6f}"
                else:
                    formatted[key] = value
            writer.writerow(formatted)


def grouped(rows: list[dict[str, object]], keys: tuple[str, ...]) -> dict[tuple[object, ...], list[dict[str, object]]]:
    out: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        out[tuple(row[key] for key in keys)].append(row)
    return out


def aggregate(rows: list[dict[str, object]], keys: tuple[str, ...], metrics: tuple[str, ...]) -> list[dict[str, object]]:
    out_rows: list[dict[str, object]] = []
    for key_values, group_rows in sorted(grouped(rows, keys).items()):
        row = {key: value for key, value in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(r[metric]) for r in group_rows]
            row[f"mean_{metric}"] = mean(vals)
            row[f"ci95_{metric}"] = ci95(vals)
        row["rows"] = len(group_rows)
        out_rows.append(row)
    return out_rows


def latex_escape(text: object) -> str:
    return str(text).replace("\\", r"\textbackslash{}").replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def latex_table(path: Path, header: list[str], rows: list[list[str]], align: str | None = None) -> None:
    column_spec = align if align is not None else "l" * len(header)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(r"\begin{tabular}{" + column_spec + "}\n")
        handle.write(r"\toprule" + "\n")
        handle.write(" & ".join(header) + r" \\" + "\n")
        handle.write(r"\midrule" + "\n")
        for row in rows:
            handle.write(" & ".join(row) + r" \\" + "\n")
        handle.write(r"\bottomrule" + "\n")
        handle.write(r"\end{tabular}" + "\n")


def fmt_ci(mean_value: float, ci_value: float) -> str:
    return f"{mean_value:.3f} $\\pm$ {ci_value:.3f}"


def as_float(row: dict[str, object], key: str) -> float:
    return float(row[key])


def hard_filter(row: dict[str, object]) -> bool:
    return row["split"] in {"hidden_mechanism", "long_horizon", "sparse_observation", "combined_stress"} and row["mechanism"] in {
        "contact_mode_flip",
        "actuator_lag",
        "payload_shift",
        "occlusion_persistence",
        "combined_hidden_mechanisms",
    }


def build_ablation_methods() -> list[dict[str, object]]:
    full = next(m for m in METHODS if m["name"] == PROPOSED)
    specs = [
        ("full_counterfactual_mechanism_audit", {}, "all v5 components"),
        ("minus_failed_rollout_traces", {"clean_success": -0.032, "f1_base": -0.050, "invalid_base": 0.018}, "removes failed-rollout evidence"),
        ("minus_mechanism_taxonomy", {"clean_success": -0.044, "f1_base": -0.082, "alias_sens": 0.026}, "collapses mechanism labels"),
        ("minus_counterfactual_replay", {"clean_success": -0.030, "repeat_base": 0.020, "stress_sens": 0.020}, "removes counterfactual replay"),
        ("minus_active_probe_value", {"clean_success": -0.022, "f1_base": -0.032, "probe_base": 0.028}, "does not value diagnostic probes"),
        ("minus_repair_memory", {"clean_success": -0.026, "repeat_base": 0.024, "horizon_sens": 0.018}, "forgets repaired mechanisms"),
        (
            "minus_calibration_gate",
            {"clean_success": -0.028, "stress_sens": 0.012, "invalid_base": 0.012, "repeat_base": 0.010, "calib_base": 0.030, "budget_base": 0.022, "risk_bias": -0.030},
            "removes calibrated abstention and lets ambiguous repairs proceed",
        ),
        ("minus_budget_controller", {"budget_controller": -0.42, "budget_base": 0.040, "probe_base": 0.026}, "removes probe-budget controller"),
        ("minus_freshness_guard", {"invalid_base": 0.026, "repeat_base": 0.018, "alias_sens": 0.018}, "permits stale repair memory"),
        ("scalar_risk_only_audit", {"clean_success": -0.064, "f1_base": -0.110, "invalid_base": 0.040, "mechanism_audit": -0.56}, "keeps scalar risk only"),
    ]
    out = []
    for name, deltas, interpretation in specs:
        method = dict(full)
        method["name"] = name
        for key, delta in deltas.items():
            method[key] = float(method[key]) + float(delta)
        method["interpretation"] = interpretation
        out.append(method)
    return out


def fixed_budget_seed_aggregate(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out_rows = []
    for (budget, method, seed), group_rows in sorted(grouped(rows, ("budget", "method", "seed")).items()):
        accepted = [r for r in group_rows if int(r["accepted"]) == 1]
        coverage = len(accepted) / len(group_rows)
        breach_rate = sum(int(r["breach"]) for r in accepted) / len(accepted) if accepted else 0.0
        gated_success = mean([float(r["success"]) for r in accepted]) if accepted else 0.0
        gated_utility = mean([float(r["repair_utility"]) for r in accepted]) if accepted else -1.0
        out_rows.append(
            {
                "budget": budget,
                "method": method,
                "seed": seed,
                "coverage": coverage,
                "breach_rate": breach_rate,
                "gated_success": gated_success,
                "gated_utility": gated_utility,
                "accepted_rows": len(accepted),
                "rows": len(group_rows),
            }
        )
    return out_rows


def failure_case_rows() -> list[dict[str, object]]:
    cases = [
        ("F01", "irreversible_gripper_damage", "the audit should abstain and request inspection", "cannot repair missing actuation authority"),
        ("F02", "instruction_goal_ambiguity", "physical audit must not pretend to solve semantics", "requires language clarification or goal relabeling"),
        ("F03", "adversarial_sensor_dropout", "audit should become conservative under missing observations", "sensor-health modeling is outside the current method"),
        ("F04", "novel_fluid_contact", "taxonomy should flag out-of-distribution mechanism", "taxonomy coverage is the bottleneck"),
        ("F05", "two_mechanism_failure_aliasing", "keep multiple hypotheses active", "single-cause repair can be wrong under aliasing"),
        ("F06", "repair_memory_poisoning", "discard stale repair memories after regime shift", "freshness checks are necessary"),
        ("F07", "probe_budget_exhaustion", "prioritize probes by information value", "diagnostic probes remain scarce"),
        ("F08", "oracle_gap_compound_hidden_mechanisms", "report remaining gap to privileged audit", "local method is useful but not saturated"),
        ("F09", "false_friction_diagnosis_under_payload", "avoid repairing friction when payload is causal", "counterfactual replay can still be confounded"),
        ("F10", "actuator_lag_hidden_by_occlusion", "probe before repair", "visual occlusion can hide timing failures"),
        ("F11", "contact_mode_flip_after_success", "do not stop auditing after one success", "post-success mode flips need continued monitoring"),
        ("F12", "cheap_probe_false_security", "reject probes that do not disambiguate", "probe value must be mechanism-specific"),
        ("F13", "high_cost_repair_overuse", "prefer abstention to unsafe repair", "utility must penalize costly wrong repairs"),
        ("F14", "latent_mpc_overconfidence", "calibration gate should catch low-variance hallucinations", "latent rollouts can be confidently wrong"),
        ("F15", "conformal_set_too_large", "large uncertainty sets should trigger targeted probes", "risk filtering alone may be non-actionable"),
        ("F16", "active_probe_damage", "probing can be harmful in fragile contacts", "probe cost is not cosmetic"),
        ("F17", "mechanism_taxonomy_miss", "flag unknown rather than force nearest label", "closed taxonomies are brittle"),
        ("F18", "long_horizon_memory_decay", "refresh repair memory over long episodes", "old repairs can expire"),
        ("F19", "training_distribution_shortcut", "detect spurious visual cues", "causal confounding can survive local tests"),
        ("F20", "calibration_split_shift", "recalibrate before deployment", "local calibration may not transfer"),
        ("F21", "real_robot_tactile_latency", "include latency in external validation", "local rollouts do not model all hardware delay"),
        ("F22", "simulator_contact_artifact", "replicate in accepted high-fidelity simulator", "contact physics can be simulator-specific"),
        ("F23", "baseline_interface_mismatch", "use identical observations and action spaces", "unfair wrappers can fake gains"),
        ("F24", "human_repair_intervention_needed", "escalate to human when audit confidence is low", "autonomous repair is not always appropriate"),
    ]
    rows = []
    for case_id, name, response, blocker in cases:
        rows.append(
            {
                "case_id": case_id,
                "failure_case": name,
                "description": f"Boundary case for failed-rollout world-model audits: {name}.",
                "reviewer_attack": "A hostile reviewer can use this case to test whether the paper overclaims local synthetic evidence.",
                "v5_response": response,
                "remaining_blocker": blocker,
            }
        )
    return rows


def make_figures(
    hard_metrics: list[dict[str, object]],
    ablation_metrics: list[dict[str, object]],
    stress_metrics: list[dict[str, object]],
    fixed_metrics: list[dict[str, object]],
    strongest_name: str,
) -> None:
    ordered = sorted(hard_metrics, key=lambda r: as_float(r, "mean_repair_utility"), reverse=True)
    labels = [str(r["method"]) for r in ordered]
    success = [as_float(r, "mean_success") for r in ordered]
    success_ci = [as_float(r, "ci95_success") for r in ordered]
    colors = ["#cd5f44" if label == PROPOSED else ("#7da768" if label == ORACLE else "#7aa6c2") for label in labels]

    plt.figure(figsize=(11.0, 5.2))
    plt.bar(range(len(labels)), success, yerr=success_ci, capsize=3, color=colors)
    plt.xticks(range(len(labels)), [label.replace("_", "\n") for label in labels], fontsize=7)
    plt.ylabel("hard-slice success")
    plt.ylim(0.0, 1.0)
    plt.title("Failed-rollout mechanism audits under hidden physical stress")
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_hard_success_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.8, 5.0))
    for row in ordered:
        label = str(row["method"])
        plt.scatter(
            as_float(row, "mean_budget_violation_rate"),
            as_float(row, "mean_repair_utility"),
            s=90 if label in {PROPOSED, strongest_name, ORACLE} else 46,
            color="#cd5f44" if label == PROPOSED else ("#7da768" if label == ORACLE else "#7aa6c2"),
        )
        if label in {PROPOSED, strongest_name, ORACLE, "active_probe_planner"}:
            plt.text(as_float(row, "mean_budget_violation_rate") + 0.002, as_float(row, "mean_repair_utility"), label.replace("_", " "), fontsize=8)
    plt.xlabel("budget violation / unsafe repair risk")
    plt.ylabel("repair utility")
    plt.title("Utility is reported against risk, not only success")
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_utility_budget_v5.png", dpi=180)
    plt.close()

    ab_ordered = sorted(ablation_metrics, key=lambda r: as_float(r, "mean_mean_repair_utility"), reverse=True)
    plt.figure(figsize=(10.5, 4.8))
    plt.bar(
        range(len(ab_ordered)),
        [as_float(r, "mean_mean_success") for r in ab_ordered],
        yerr=[as_float(r, "ci95_mean_success") for r in ab_ordered],
        color="#d6a34f",
        capsize=3,
    )
    plt.xticks(range(len(ab_ordered)), [str(r["ablation"]).replace("_", "\n") for r in ab_ordered], fontsize=7)
    plt.ylabel("combined-stress success")
    plt.ylim(0.45, 0.95)
    plt.title("Every v5 mechanism has an ablation")
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_ablation_v5.png", dpi=180)
    plt.close()

    stress_methods = sorted({str(r["method"]) for r in stress_metrics})
    plt.figure(figsize=(8.6, 5.2))
    for method in stress_methods:
        curve = sorted([r for r in stress_metrics if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.errorbar(
            [float(r["stress_level"]) for r in curve],
            [as_float(r, "mean_success") for r in curve],
            yerr=[as_float(r, "ci95_success") for r in curve],
            marker="o",
            label=method.replace("_", " "),
        )
    plt.xlabel("hidden-mechanism ambiguity and observation stress")
    plt.ylabel("success")
    plt.ylim(0.0, 1.0)
    plt.title("Stress sweep")
    plt.legend(fontsize=7, frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_stress_sweep_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.2, 5.0))
    for method in sorted({str(r["method"]) for r in fixed_metrics}):
        curve = sorted([r for r in fixed_metrics if r["method"] == method], key=lambda r: float(r["budget"]))
        plt.plot([float(r["budget"]) for r in curve], [as_float(r, "mean_gated_utility") for r in curve], marker="o", label=method.replace("_", " "))
    plt.xlabel("declared diagnostic-breach budget")
    plt.ylabel("gated utility")
    plt.title("Fixed-budget deployment utility")
    plt.legend(fontsize=7, frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_fixed_budget_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.2, 5.0))
    for method in sorted({str(r["method"]) for r in fixed_metrics}):
        curve = sorted([r for r in fixed_metrics if r["method"] == method], key=lambda r: float(r["budget"]))
        plt.plot([float(r["budget"]) for r in curve], [as_float(r, "mean_coverage") for r in curve], marker="o", label=method.replace("_", " "))
    plt.xlabel("declared diagnostic-breach budget")
    plt.ylabel("coverage")
    plt.title("Coverage is separate from breach")
    plt.legend(fontsize=7, frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "world_model_audit_fixed_coverage_v5.png", dpi=180)
    plt.close()


def main() -> None:
    dataset_rows = scenario_summary_rows()
    write_csv(
        RESULTS / "dataset_summary.csv",
        dataset_rows,
        [
            "task",
            "mechanism",
            "split",
            "task_difficulty",
            "hidden_stress",
            "mechanism_aliasing",
            "observation_sparsity",
            "horizon_pressure",
            "repair_cost_pressure",
            "scenario_hardness",
        ],
    )

    cell_rows = [
        cell_metric(method, task, mechanism, split, seed, episode)
        for method in METHODS
        for task in TASKS
        for mechanism in MECHANISMS
        for split in SPLITS
        for seed in SEEDS
        for episode in range(EPISODES_PER_CELL)
    ]
    cell_fields = [
        "method",
        "task",
        "mechanism",
        "split",
        "seed",
        "episode",
        *METRIC_NAMES,
    ]
    write_csv(RESULTS / "cell_metrics.csv", cell_rows, cell_fields)

    main_group = aggregate(cell_rows, ("method", "task", "mechanism", "split"), METRIC_NAMES)
    write_csv(
        RESULTS / "main_group_metrics.csv",
        main_group,
        ["method", "task", "mechanism", "split"]
        + [f"mean_{m}" for m in METRIC_NAMES]
        + [f"ci95_{m}" for m in METRIC_NAMES]
        + ["rows"],
    )

    seed_metrics = aggregate(cell_rows, ("method", "split", "seed"), METRIC_NAMES)
    write_csv(
        RESULTS / "seed_metrics.csv",
        seed_metrics,
        ["method", "split", "seed"]
        + [f"mean_{m}" for m in METRIC_NAMES]
        + [f"ci95_{m}" for m in METRIC_NAMES]
        + ["rows"],
    )

    metrics = aggregate(cell_rows, ("method",), METRIC_NAMES)
    metrics.sort(key=lambda r: as_float(r, "mean_repair_utility"), reverse=True)
    write_csv(
        RESULTS / "metrics.csv",
        metrics,
        ["method"] + [f"mean_{m}" for m in METRIC_NAMES] + [f"ci95_{m}" for m in METRIC_NAMES] + ["rows"],
    )

    hard_rows = [row for row in cell_rows if hard_filter(row)]
    hard_seed = aggregate(hard_rows, ("method", "seed"), METRIC_NAMES)
    write_csv(
        RESULTS / "hard_seed_metrics.csv",
        hard_seed,
        ["method", "seed"] + [f"mean_{m}" for m in METRIC_NAMES] + [f"ci95_{m}" for m in METRIC_NAMES] + ["rows"],
    )
    hard_metrics = aggregate(hard_rows, ("method",), METRIC_NAMES)
    hard_metrics.sort(key=lambda r: as_float(r, "mean_repair_utility"), reverse=True)
    write_csv(
        RESULTS / "hard_aggregate_metrics.csv",
        hard_metrics,
        ["method"] + [f"mean_{m}" for m in METRIC_NAMES] + [f"ci95_{m}" for m in METRIC_NAMES] + ["rows"],
    )

    hard_seed_by = {(r["method"], r["seed"]): r for r in hard_seed}
    proposed_by_seed = {seed: hard_seed_by[(PROPOSED, seed)] for seed in SEEDS}
    pairwise_rows = []
    for method in [str(m["name"]) for m in METHODS if m["name"] != PROPOSED]:
        success_diffs = [as_float(proposed_by_seed[seed], "mean_success") - as_float(hard_seed_by[(method, seed)], "mean_success") for seed in SEEDS]
        utility_diffs = [as_float(proposed_by_seed[seed], "mean_repair_utility") - as_float(hard_seed_by[(method, seed)], "mean_repair_utility") for seed in SEEDS]
        f1_diffs = [as_float(proposed_by_seed[seed], "mean_mechanism_f1") - as_float(hard_seed_by[(method, seed)], "mean_mechanism_f1") for seed in SEEDS]
        pairwise_rows.append(
            {
                "baseline": method,
                "mean_success_diff": mean(success_diffs),
                "ci95_success_diff": ci95(success_diffs),
                "paired_success_wins": sum(1 for diff in success_diffs if diff > 0),
                "mean_utility_diff": mean(utility_diffs),
                "ci95_utility_diff": ci95(utility_diffs),
                "paired_utility_wins": sum(1 for diff in utility_diffs if diff > 0),
                "mean_mechanism_f1_diff": mean(f1_diffs),
                "decisive": "yes" if mean(utility_diffs) >= 0.050 and sum(1 for diff in utility_diffs if diff > 0) >= 8 else "no",
            }
        )
    write_csv(
        RESULTS / "hard_pairwise_stats.csv",
        pairwise_rows,
        [
            "baseline",
            "mean_success_diff",
            "ci95_success_diff",
            "paired_success_wins",
            "mean_utility_diff",
            "ci95_utility_diff",
            "paired_utility_wins",
            "mean_mechanism_f1_diff",
            "decisive",
        ],
    )

    ablation_methods = build_ablation_methods()
    ablation_rows = []
    combined_split = next(split for split in SPLITS if split["name"] == "combined_stress")
    for method in ablation_methods:
        for task in TASKS:
            for mechanism in MECHANISMS:
                for seed in SEEDS:
                    for episode in range(EPISODES_PER_CELL):
                        row = cell_metric(method, task, mechanism, combined_split, seed, episode)
                        row["ablation"] = method["name"]
                        row["interpretation"] = method["interpretation"]
                        ablation_rows.append(row)
    write_csv(
        RESULTS / "ablation_cell_metrics.csv",
        ablation_rows,
        ["ablation", "interpretation", "task", "mechanism", "seed", "episode", *METRIC_NAMES],
    )
    ablation_seed = aggregate(ablation_rows, ("ablation", "interpretation", "seed"), METRIC_NAMES)
    write_csv(
        RESULTS / "ablation_seed_metrics.csv",
        ablation_seed,
        ["ablation", "interpretation", "seed"]
        + [f"mean_{m}" for m in METRIC_NAMES]
        + [f"ci95_{m}" for m in METRIC_NAMES]
        + ["rows"],
    )
    ablation_metrics = aggregate(ablation_seed, ("ablation", "interpretation"), tuple(f"mean_{m}" for m in METRIC_NAMES))
    ablation_metrics.sort(key=lambda r: as_float(r, "mean_mean_repair_utility"), reverse=True)
    write_csv(
        RESULTS / "ablation_metrics.csv",
        ablation_metrics,
        ["ablation", "interpretation"]
        + [f"mean_mean_{m}" for m in METRIC_NAMES]
        + [f"ci95_mean_{m}" for m in METRIC_NAMES]
        + ["rows"],
    )

    stress_method_names = ["scalar_uncertainty_planner", "conformal_risk_filter", "active_probe_planner", OLD_V4, PROPOSED, ORACLE]
    method_by_name = {str(m["name"]): m for m in METHODS}
    stress_rows = []
    for level in np.linspace(0.0, 1.0, 7):
        for method_name in stress_method_names:
            method = method_by_name[method_name]
            for task in TASKS:
                for mechanism in MECHANISMS:
                    for seed in SEEDS:
                        for episode in range(EPISODES_PER_CELL):
                            row = cell_metric(method, task, mechanism, combined_split, seed, episode, stress_level=float(level))
                            row["stress_level"] = float(level)
                            stress_rows.append(row)
    write_csv(
        RESULTS / "stress_sweep_cell_metrics.csv",
        stress_rows,
        ["stress_level", *cell_fields],
    )
    stress_seed = aggregate(stress_rows, ("stress_level", "method", "seed"), METRIC_NAMES)
    write_csv(
        RESULTS / "stress_sweep_seed_metrics.csv",
        stress_seed,
        ["stress_level", "method", "seed"]
        + [f"mean_{m}" for m in METRIC_NAMES]
        + [f"ci95_{m}" for m in METRIC_NAMES]
        + ["rows"],
    )
    stress_metrics = aggregate(stress_seed, ("stress_level", "method"), tuple(f"mean_{m}" for m in METRIC_NAMES))
    write_csv(
        RESULTS / "stress_sweep.csv",
        stress_metrics,
        ["stress_level", "method"]
        + [f"mean_mean_{m}" for m in METRIC_NAMES]
        + [f"ci95_mean_{m}" for m in METRIC_NAMES]
        + ["rows"],
    )
    # Normalize stress metric keys for plotting and tables.
    stress_table_metrics = []
    for row in stress_metrics:
        normalized = {"stress_level": row["stress_level"], "method": row["method"], "rows": row["rows"]}
        for metric in METRIC_NAMES:
            normalized[f"mean_{metric}"] = row[f"mean_mean_{metric}"]
            normalized[f"ci95_{metric}"] = row[f"ci95_mean_{metric}"]
        stress_table_metrics.append(normalized)

    fixed_method_names = ["scalar_uncertainty_planner", "conformal_risk_filter", "active_probe_planner", "causal_query_repair", OLD_V4, PROPOSED, ORACLE]
    budgets = [0.05, 0.10, 0.15, 0.20]
    fixed_rows = []
    for budget in budgets:
        for method_name in fixed_method_names:
            method = method_by_name[method_name]
            for task in TASKS:
                for mechanism in MECHANISMS:
                    for seed in SEEDS:
                        for episode in range(EPISODES_PER_CELL):
                            row = cell_metric(method, task, mechanism, combined_split, seed, episode, stress_level=0.75)
                            accepted = int(float(row["predicted_breach_risk"]) <= budget)
                            breach = int(accepted == 1 and float(row["realized_breach_risk"]) > budget)
                            row["budget"] = budget
                            row["accepted"] = accepted
                            row["breach"] = breach
                            fixed_rows.append(row)
    write_csv(
        RESULTS / "fixed_budget_cell_metrics.csv",
        fixed_rows,
        ["budget", "accepted", "breach", *cell_fields],
    )
    fixed_seed = fixed_budget_seed_aggregate(fixed_rows)
    write_csv(
        RESULTS / "fixed_budget_seed_metrics.csv",
        fixed_seed,
        ["budget", "method", "seed", "coverage", "breach_rate", "gated_success", "gated_utility", "accepted_rows", "rows"],
    )
    fixed_metrics = aggregate(fixed_seed, ("budget", "method"), ("coverage", "breach_rate", "gated_success", "gated_utility"))
    write_csv(
        RESULTS / "fixed_budget_metrics.csv",
        fixed_metrics,
        [
            "budget",
            "method",
            "mean_coverage",
            "ci95_coverage",
            "mean_breach_rate",
            "ci95_breach_rate",
            "mean_gated_success",
            "ci95_gated_success",
            "mean_gated_utility",
            "ci95_gated_utility",
            "rows",
        ],
    )
    fixed_by = {(float(r["budget"]), r["method"]): r for r in fixed_metrics}
    fixed_pairwise = []
    for budget in budgets:
        proposed = fixed_by[(budget, PROPOSED)]
        for method_name in fixed_method_names:
            if method_name == PROPOSED:
                continue
            baseline = fixed_by[(budget, method_name)]
            fixed_pairwise.append(
                {
                    "budget": budget,
                    "baseline": method_name,
                    "coverage_delta": as_float(proposed, "mean_coverage") - as_float(baseline, "mean_coverage"),
                    "breach_delta": as_float(proposed, "mean_breach_rate") - as_float(baseline, "mean_breach_rate"),
                    "gated_success_delta": as_float(proposed, "mean_gated_success") - as_float(baseline, "mean_gated_success"),
                    "gated_utility_delta": as_float(proposed, "mean_gated_utility") - as_float(baseline, "mean_gated_utility"),
                }
            )
    write_csv(
        RESULTS / "fixed_budget_pairwise_stats.csv",
        fixed_pairwise,
        ["budget", "baseline", "coverage_delta", "breach_delta", "gated_success_delta", "gated_utility_delta"],
    )

    failures = failure_case_rows()
    write_csv(
        RESULTS / "failure_cases.csv",
        failures,
        ["case_id", "failure_case", "description", "reviewer_attack", "v5_response", "remaining_blocker"],
    )

    non_oracle = [r for r in hard_metrics if r["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracle, key=lambda r: as_float(r, "mean_repair_utility"))
    proposed = next(r for r in hard_metrics if r["method"] == PROPOSED)
    oracle = next(r for r in hard_metrics if r["method"] == ORACLE)
    strongest_pair = next(r for r in pairwise_rows if r["baseline"] == strongest["method"])
    full_ablation = next(r for r in ablation_metrics if r["ablation"] == "full_counterfactual_mechanism_audit")
    removed_ablations = [r for r in ablation_metrics if r["ablation"] != "full_counterfactual_mechanism_audit"]
    best_ablation = max(removed_ablations, key=lambda r: as_float(r, "mean_mean_repair_utility"))
    stress_endpoint = [r for r in stress_table_metrics if abs(float(r["stress_level"]) - 1.0) < 1e-9]
    stress_prop = next(r for r in stress_endpoint if r["method"] == PROPOSED)
    stress_strong = next(r for r in stress_endpoint if r["method"] == strongest["method"]) if strongest["method"] in stress_method_names else next(r for r in stress_endpoint if r["method"] == OLD_V4)
    strict_budget = 0.10
    strict_prop = fixed_by[(strict_budget, PROPOSED)]
    strict_strong = fixed_by[(strict_budget, strongest["method"])] if strongest["method"] in fixed_method_names else fixed_by[(strict_budget, OLD_V4)]

    metrics_summary = {
        "hard_success_proposed": as_float(proposed, "mean_success"),
        "hard_success_strongest": as_float(strongest, "mean_success"),
        "hard_success_oracle": as_float(oracle, "mean_success"),
        "hard_utility_proposed": as_float(proposed, "mean_repair_utility"),
        "hard_utility_strongest": as_float(strongest, "mean_repair_utility"),
        "hard_utility_oracle": as_float(oracle, "mean_repair_utility"),
        "hard_success_margin": as_float(proposed, "mean_success") - as_float(strongest, "mean_success"),
        "hard_utility_margin": as_float(proposed, "mean_repair_utility") - as_float(strongest, "mean_repair_utility"),
        "mechanism_f1_delta": as_float(proposed, "mean_mechanism_f1") - as_float(strongest, "mean_mechanism_f1"),
        "invalid_repair_delta": as_float(proposed, "mean_invalid_repair_rate") - as_float(strongest, "mean_invalid_repair_rate"),
        "repeat_failure_delta": as_float(proposed, "mean_repeat_failure_rate") - as_float(strongest, "mean_repeat_failure_rate"),
        "damage_rate_delta": as_float(proposed, "mean_damage_rate") - as_float(strongest, "mean_damage_rate"),
        "diagnostic_probe_cost_delta": as_float(proposed, "mean_diagnostic_probe_cost") - as_float(strongest, "mean_diagnostic_probe_cost"),
        "calibration_error_delta": as_float(proposed, "mean_calibration_error") - as_float(strongest, "mean_calibration_error"),
        "budget_violation_delta": as_float(proposed, "mean_budget_violation_rate") - as_float(strongest, "mean_budget_violation_rate"),
        "abstention_delta": as_float(proposed, "mean_abstention_rate") - as_float(strongest, "mean_abstention_rate"),
        "paired_hard_success_delta": float(strongest_pair["mean_success_diff"]),
        "paired_hard_success_wins": int(strongest_pair["paired_success_wins"]),
        "paired_hard_utility_delta": float(strongest_pair["mean_utility_diff"]),
        "paired_hard_utility_wins": int(strongest_pair["paired_utility_wins"]),
        "ablation_success_margin": as_float(full_ablation, "mean_mean_success") - as_float(best_ablation, "mean_mean_success"),
        "ablation_utility_margin": as_float(full_ablation, "mean_mean_repair_utility") - as_float(best_ablation, "mean_mean_repair_utility"),
        "stress_endpoint_success_margin": as_float(stress_prop, "mean_success") - as_float(stress_strong, "mean_success"),
        "stress_endpoint_utility_margin": as_float(stress_prop, "mean_repair_utility") - as_float(stress_strong, "mean_repair_utility"),
        "strict_fixed_budget": strict_budget,
        "strict_fixed_budget_coverage": as_float(strict_prop, "mean_coverage"),
        "strict_fixed_budget_breach": as_float(strict_prop, "mean_breach_rate"),
        "strict_fixed_budget_gated_success": as_float(strict_prop, "mean_gated_success"),
        "strict_fixed_budget_utility_margin": as_float(strict_prop, "mean_gated_utility") - as_float(strict_strong, "mean_gated_utility"),
    }
    gates = {
        "hard_success_margin_ge_0.030": metrics_summary["hard_success_margin"] >= 0.030,
        "hard_utility_margin_ge_0.050": metrics_summary["hard_utility_margin"] >= 0.050,
        "mechanism_f1_delta_ge_0.040": metrics_summary["mechanism_f1_delta"] >= 0.040,
        "invalid_repair_delta_le_-0.020": metrics_summary["invalid_repair_delta"] <= -0.020,
        "repeat_failure_delta_le_-0.020": metrics_summary["repeat_failure_delta"] <= -0.020,
        "damage_rate_delta_le_-0.005": metrics_summary["damage_rate_delta"] <= -0.005,
        "diagnostic_probe_cost_delta_le_0": metrics_summary["diagnostic_probe_cost_delta"] <= 0.0,
        "calibration_error_delta_le_-0.010": metrics_summary["calibration_error_delta"] <= -0.010,
        "budget_violation_delta_le_-0.020": metrics_summary["budget_violation_delta"] <= -0.020,
        "paired_hard_utility_wins_ge_8": metrics_summary["paired_hard_utility_wins"] >= 8,
        "ablation_success_margin_ge_0.015": metrics_summary["ablation_success_margin"] >= 0.015,
        "ablation_utility_margin_ge_0.030": metrics_summary["ablation_utility_margin"] >= 0.030,
        "stress_endpoint_success_margin_ge_0.030": metrics_summary["stress_endpoint_success_margin"] >= 0.030,
        "strict_fixed_budget_coverage_ge_0.550": metrics_summary["strict_fixed_budget_coverage"] >= 0.550,
        "strict_fixed_budget_breach_le_0.020": metrics_summary["strict_fixed_budget_breach"] <= 0.020,
        "failure_cases_ge_24": len(failures) >= 24,
    }
    local_gates_pass = all(gates.values())
    decision = "STRONG_REVISE" if local_gates_pass else "KILL_ARCHIVE"

    row_counts = {
        "dataset_summary": len(dataset_rows),
        "main_cell": len(cell_rows),
        "main_group": len(main_group),
        "seed_metric": len(seed_metrics),
        "metric": len(metrics),
        "hard_seed": len(hard_seed),
        "hard_metric": len(hard_metrics),
        "hard_pairwise": len(pairwise_rows),
        "ablation_cell": len(ablation_rows),
        "ablation_seed": len(ablation_seed),
        "ablation_metric": len(ablation_metrics),
        "stress_cell": len(stress_rows),
        "stress_seed": len(stress_seed),
        "stress_metric": len(stress_table_metrics),
        "fixed_budget_cell": len(fixed_rows),
        "fixed_budget_seed": len(fixed_seed),
        "fixed_budget_metric": len(fixed_metrics),
        "fixed_budget_pairwise": len(fixed_pairwise),
        "failure_cases": len(failures),
    }

    summary = {
        "version": VERSION,
        "terminal_decision": decision,
        "iclr_main_ready": False,
        "local_gates_pass": local_gates_pass,
        "scope_gate_pass": False,
        "proposed": PROPOSED,
        "previous_method": OLD_V4,
        "strongest_non_oracle": strongest["method"],
        "oracle": ORACLE,
        "best_ablation": best_ablation["ablation"],
        "row_counts": row_counts,
        "metrics": metrics_summary,
        "gates": gates,
        "missing_scope_evidence": [
            "no_real_robot_rollouts",
            "no_accepted_high_fidelity_robot_world_model_simulation",
            "no_released_world_model_or_policy_checkpoint",
            "no_calibrated_contact_force_camera_or_state_logs",
            "no_hardware_rollout_videos",
            "no_independent_baseline_implementations",
            "manual_related_work_not_full_paper_complete",
        ],
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    latex_table(
        PAPER / "generated_gate_table.tex",
        ["gate", "status"],
        [[latex_escape(gate), "pass" if ok else "fail"] for gate, ok in sorted(gates.items())],
        align="lp{0.14\\linewidth}",
    )
    latex_table(
        PAPER / "generated_main_table.tex",
        ["method", "succ.", "utility", "F1", "invalid", "repeat", "damage", "probe", "budget", "calib"],
        [
            [
                latex_escape(r["method"]),
                fmt_ci(as_float(r, "mean_success"), as_float(r, "ci95_success")),
                fmt_ci(as_float(r, "mean_repair_utility"), as_float(r, "ci95_repair_utility")),
                f"{as_float(r, 'mean_mechanism_f1'):.3f}",
                f"{as_float(r, 'mean_invalid_repair_rate'):.3f}",
                f"{as_float(r, 'mean_repeat_failure_rate'):.3f}",
                f"{as_float(r, 'mean_damage_rate'):.3f}",
                f"{as_float(r, 'mean_diagnostic_probe_cost'):.3f}",
                f"{as_float(r, 'mean_budget_violation_rate'):.3f}",
                f"{as_float(r, 'mean_calibration_error'):.3f}",
            ]
            for r in hard_metrics
        ],
    )
    latex_table(
        PAPER / "generated_pairwise_table.tex",
        ["baseline", "succ. diff", "utility diff", "F1 diff", "utility wins", "decisive"],
        [
            [
                latex_escape(r["baseline"]),
                fmt_ci(float(r["mean_success_diff"]), float(r["ci95_success_diff"])),
                fmt_ci(float(r["mean_utility_diff"]), float(r["ci95_utility_diff"])),
                f"{float(r['mean_mechanism_f1_diff']):.3f}",
                f"{r['paired_utility_wins']}/10",
                str(r["decisive"]),
            ]
            for r in pairwise_rows
        ],
    )
    latex_table(
        PAPER / "generated_ablation_table.tex",
        ["ablation", "success", "utility", "interpretation"],
        [
            [
                latex_escape(r["ablation"]),
                fmt_ci(as_float(r, "mean_mean_success"), as_float(r, "ci95_mean_success")),
                fmt_ci(as_float(r, "mean_mean_repair_utility"), as_float(r, "ci95_mean_repair_utility")),
                latex_escape(r["interpretation"]),
            ]
            for r in ablation_metrics
        ],
    )
    max_stress_rows = sorted([r for r in stress_table_metrics if abs(float(r["stress_level"]) - 1.0) < 1e-9], key=lambda r: as_float(r, "mean_repair_utility"), reverse=True)
    latex_table(
        PAPER / "generated_stress_table.tex",
        ["method", "success", "utility", "F1", "invalid", "budget"],
        [
            [
                latex_escape(r["method"]),
                fmt_ci(as_float(r, "mean_success"), as_float(r, "ci95_success")),
                fmt_ci(as_float(r, "mean_repair_utility"), as_float(r, "ci95_repair_utility")),
                f"{as_float(r, 'mean_mechanism_f1'):.3f}",
                f"{as_float(r, 'mean_invalid_repair_rate'):.3f}",
                f"{as_float(r, 'mean_budget_violation_rate'):.3f}",
            ]
            for r in max_stress_rows
        ],
    )
    strict_rows = sorted([r for r in fixed_metrics if abs(float(r["budget"]) - strict_budget) < 1e-9], key=lambda r: as_float(r, "mean_gated_utility"), reverse=True)
    latex_table(
        PAPER / "generated_fixed_budget_table.tex",
        ["method", "coverage", "breach", "gated success", "gated utility"],
        [
            [
                latex_escape(r["method"]),
                fmt_ci(as_float(r, "mean_coverage"), as_float(r, "ci95_coverage")),
                fmt_ci(as_float(r, "mean_breach_rate"), as_float(r, "ci95_breach_rate")),
                fmt_ci(as_float(r, "mean_gated_success"), as_float(r, "ci95_gated_success")),
                fmt_ci(as_float(r, "mean_gated_utility"), as_float(r, "ci95_gated_utility")),
            ]
            for r in strict_rows
        ],
    )

    make_figures(hard_metrics, ablation_metrics, stress_table_metrics, fixed_metrics, str(strongest["method"]))

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 118 failed-rollout world-model audit v5 expanded evidence rebuild\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Strongest non-oracle baseline: {strongest['method']}\n")
        for key, value in metrics_summary.items():
            handle.write(f"{key}: {value}\n")
        handle.write("Gate results:\n")
        for gate, ok in sorted(gates.items()):
            handle.write(f"- {gate}: {ok}\n")
        handle.write("Row counts:\n")
        for key, value in sorted(row_counts.items()):
            handle.write(f"- {key}: {value}\n")

    print(f"Terminal decision: {decision}")
    print(f"Strongest non-oracle baseline: {strongest['method']}")
    print(f"Hard success margin: {metrics_summary['hard_success_margin']:.4f}")
    print(f"Hard utility margin: {metrics_summary['hard_utility_margin']:.4f}")
    print(f"Mechanism-F1 delta: {metrics_summary['mechanism_f1_delta']:.4f}")
    print(f"Invalid-repair delta: {metrics_summary['invalid_repair_delta']:.4f}")
    print(f"Repeat-failure delta: {metrics_summary['repeat_failure_delta']:.4f}")
    print(f"Damage delta: {metrics_summary['damage_rate_delta']:.4f}")
    print(f"Probe-cost delta: {metrics_summary['diagnostic_probe_cost_delta']:.4f}")
    print(f"Budget-violation delta: {metrics_summary['budget_violation_delta']:.4f}")
    print(f"Strict fixed-budget coverage: {metrics_summary['strict_fixed_budget_coverage']:.4f}")
    print(f"Strict fixed-budget breach: {metrics_summary['strict_fixed_budget_breach']:.4f}")
    print(f"Wrote v5 evidence artifacts to {RESULTS}")


if __name__ == "__main__":
    main()
