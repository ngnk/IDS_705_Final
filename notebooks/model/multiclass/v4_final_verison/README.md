# IDS 705 Final Report — Evidence Archive

This folder is the cleaned archive for the multiclass World Cup match-outcome modeling report. It contains only the notebooks that directly underpin claims in the final report, organized in run order. Exploratory notebooks from `v2_integration/` are not included; they remain available there as working history.

## Model Names Used in the Report

| Name | Algorithm | Training window | Feature set |
|---|---|---|---|
| **Baseline** | Random Forest (`class_weight='balanced'`) | 2006–2014 | Team-level only (46 features) |
| **Team-history** | Random Forest (`class_weight='balanced'`) | 1998–2014 | Team-level only (46 features) |
| **Player-informed** | XGBoost | 2006–2014 | Team + player/squad (88 features) |

All models are evaluated on the held-out 2018 and 2022 World Cups (128 matches).

## Run Order

| # | Notebook | Purpose | Key outputs |
|---|---|---|---|
| 1 | `01_features_team.ipynb` | Build team-level match, history, ranking, and tournament-context features | `data/features_team.parquet` |
| 2 | `02_features_player_squad.ipynb` | Build player and squad enrichment features | `data/features_player_squad.parquet` |
| 3 | `03_interpretability.ipynb` | SHAP global importance and LIME local explanations for selected predictions | SHAP/LIME figures in `data/` |
| 4 | `04_model_lock_and_core_results.ipynb` | Lock the final three model pipelines and produce core holdout metrics | `data/final_report_lock/` |
| 5 | `05_uncertainty_and_cv_audit.ipynb` | Bootstrap CIs for Table 1, stage-wise differences, regional reliability, CV timing | `data/uncertainty_audit/` |
| 6 | `06_temporal_validation_leakage_audit.ipynb` | Audit temporal leakage in LOTO CV; compare leakage-safe alternatives | `data/cv_leakage_audit/` |
| 7 | `07_final_validation_framework_results.ipynb` | Expanding-window sensitivity check; consolidate revised-report validation numbers | `data/final_validation_framework/` |
| 8 | `08_algorithm_sensitivity.ipynb` | Unified-algorithm sensitivity check (Appendix D): isolates feature vs. algorithm effects | `data/unified_xgb_sensitivity/` |

Notebooks 1–4 must run before 5–8. Within 5–8, notebooks are independent and can be run in any order.

## Report Assets (`docs/`)

| File | Contents |
|---|---|
| `generate_optimized_figures.py` | Figure generation script |
| `figures/` | All report figures as static exports |

## Evidence Map

| Report claim | Primary evidence |
|---|---|
| Accuracy is tightly clustered across all three models | `data/final_report_lock/table1_summary.csv` |
| Accuracy alone is insufficient; draw/upset rates matter | `data/uncertainty_audit/context_baselines.csv` |
| Player-informed and baseline share the same overall accuracy; macro-F1 point estimates differ | `data/final_report_lock/table1_summary.csv`; `04_model_lock_and_core_results.ipynb` |
| Knockout-stage advantage for player-informed, but uncertainty is wide | `data/uncertainty_audit/stage_pairwise_differences.csv` |
| Group-stage differences are small and not significant | `data/uncertainty_audit/stage_uncertainty.csv` |
| LOTO CV has temporal leakage risk | `data/cv_leakage_audit/current_loto_leakage_audit.csv` |
| Expanding-window validation confirms findings hold | `data/final_validation_framework/expanding_window_sensitivity_summary.csv` |
| Player-feature macro-F1 advantage is a feature–algorithm interaction, not a standalone feature effect | `data/unified_xgb_sensitivity/verdict_unified_rf.csv`; `docs/appendix_algorithm_sensitivity.md` |
| Knockout predictions are identical under unified RF (player-informed adds nothing without XGBoost) | `data/unified_xgb_sensitivity/bootstrap_pairwise_unified_rf.csv` |
| Regional and small-sample reliability requires uncertainty communication | `data/uncertainty_audit/confederation_accuracy_uncertainty.csv` |
