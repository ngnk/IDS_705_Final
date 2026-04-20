# World Cup Analytics — Modeling Summary

**Course:** IDS-705 Machine Learning Principles, Duke University (Spring 2026)  
**Dataset:** Men's FIFA World Cup matches, filtered to **2006–2022** (313 match-level rows, 183 features)  
**Primary target:** `y_win` — 1 if home team wins, 0 otherwise (47% / 53% split)

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Data Pipeline](#2-data-pipeline)
3. [Feature Groups](#3-feature-groups)
4. [Modeling Work](#4-modeling-work)
   - [v1 — Baseline Multiclass (Elo)](#41-v1--baseline-multiclass-elo)
   - [Player Model v3](#42-player-model-v3)
   - [v2 — Integrated Features](#43-v2--integrated-features)
   - [Regression — Goal Difference](#44-regression--goal-difference)
   - [v3 — Advanced Ensemble](#45-v3--advanced-ensemble)
5. [Cross-Notebook Comparison](#5-cross-notebook-comparison)
6. [Key Findings](#6-key-findings)
7. [Open Questions](#7-open-questions)

---

## 1. Project Structure

```
notebooks/
├── eda/
│   ├── 01_class_a_feature_table.ipynb        # Base feature table construction
│   ├── 02_men_win_notwin.ipynb               # Win/no-win analysis with LOO-CV
│   ├── 03_since_1930_distribution_shift.ipynb # Temporal distribution analysis
│   ├── 04_player_club_vs_wc_performance.ipynb # Club strength vs WC performance EDA
│   └── 05_player_eda.ipynb                   # Player-level stats deep dive
│
├── features/
│   ├── 01_match_process.ipynb                # Raw match data preprocessing
│   ├── 02_player_rosters.ipynb               # Player roster aggregation
│   ├── 03_player_stats_v1.ipynb              # Initial player club stats
│   ├── 04_rankings_integration.ipynb         # Elo + FIFA rankings merge (2006–2022)
│   ├── 05_squad_level_features.ipynb         # Squad-level club stat aggregations
│   └── 06_player_stats_v2.ipynb              # Refined player stats
│
└── model/
    ├── player_model_v3.ipynb                 # Player club stats → 3-class prediction
    ├── regression/
    │   └── goal_diff_model.ipynb             # Predict goal margin (regression)
    └── multiclass/
        ├── model_comparison.ipynb            # ← Project-wide results summary
        ├── v1_baseline/
        │   └── multiclass_elo_model.ipynb    # End-to-end 3-class baseline
        ├── v2_integration/
        │   ├── 01_features_team.ipynb
        │   ├── 02_features_player_squad.ipynb
        │   ├── 03_model_training.ipynb       # 2×2 experimental design
        │   └── 04_interpretability.ipynb
        └── v3_ensemble/
            └── advanced_ensemble.ipynb       # LightGBM + stacking (binary)

data/
├── raw/
│   ├── worldcup/worldcup.db                  # Source SQLite database
│   ├── elo_ratings.csv                        # World Football Elo (1901–2023)
│   ├── fifa_ranking-2024-06-20.csv            # FIFA rankings (1992–2024)
│   ├── club_elo_ratings.csv                   # Club Elo API snapshots (2006–2022)
│   ├── player_stats_prior_season.csv          # Transfermarkt club stats
│   ├── player_rosters.csv                     # WC squad lists
│   └── teams.csv                              # team_id → team_name bridge
│
└── processed/
    ├── class_a_match_level.csv                # Base ML dataset (1248 × 104)
    ├── class_a_with_rankings.csv              # + Elo & FIFA rankings (1248 × 115)
    ├── class_a_with_squad_features.csv        # + squad club features (1248 × 183)
    ├── class_a_with_rankings_2006_2022.csv    # Filtered to 2006–2022 (488 × 115)
    ├── class_a_squad_2006_2022.csv            # ← GOLD DATASET (313 × 183)
    ├── player_stats_with_club_elo.csv         # Player stats enriched with Club Elo
    └── squad_level_features.csv               # Squad-level aggregations (158 × 34)
```

---

## 2. Data Pipeline

The full feature pipeline runs in sequence through the `notebooks/features/` notebooks:

```
worldcup.db  ──► 01_match_process ──► class_a_match_level.csv
                                              │
                 player_stats_prior_season ──► 05_squad_level_features ──► squad-level cols
                 club_elo_ratings             │
                                              │
                 elo_ratings.csv         ──► 04_rankings_integration ──► class_a_with_rankings
                 fifa_ranking.csv             │
                                              ▼
                                  class_a_squad_2006_2022.csv  (GOLD — 313 × 183)
```

**Leakage prevention:** All features use only information available *before* the match kicks off:
- Elo ratings: year-end snapshot from the year *prior* to the tournament
- FIFA rankings: last published snapshot before tournament kickoff
- Club stats: prior season only (not the season the WC takes place in)
- Historical stats: all prior World Cups, never including the current one

---

## 3. Feature Groups

The gold dataset (`class_a_squad_2006_2022.csv`) contains **183 columns** across 7 groups:

| Group | # Cols | Description |
|---|---|---|
| Engineered diffs (`feat_*`) | 25 | Home minus away comparisons (Elo diff, FIFA rank diff, squad strength diff, etc.) |
| Historical stats | 34 | Per-team prior WC record: win rate, goal diff, KO rate, PSO rate (Laplace-smoothed) |
| Squad demographics | 94 | Age, position counts, prior WC experience, squad continuity (Jaccard overlap) |
| Club performance | 79 | Avg club Elo, % elite clubs, fwd goals/assists, GK clean sheets, minutes by position |
| Rankings | 9 | National team Elo rating, FIFA rank, FIFA points (home + away + diff) |
| Match context | 11 | Group/KO stage, rest days, stadium capacity, n_referees |
| Manager features | 4 | Prior WC appearances, consecutive WC streak with same team |

### Key engineered features

| Feature | Definition |
|---|---|
| `feat_elo_rating_diff` | Home Elo − Away Elo (pre-tournament year-end) |
| `feat_fifa_rank_diff` | Away FIFA rank − Home FIFA rank (lower rank = better) |
| `feat_squad_club_strength_diff` | Home avg club Elo − Away avg club Elo |
| `feat_squad_elite_pct_diff` | Home % elite-club players − Away % elite-club players |
| `feat_squad_fwd_goals_diff` | Home fwd avg goals last season − Away fwd avg goals last season |
| `feat_squad_gk_clean_sheets_diff` | Home GK clean sheet rate − Away GK clean sheet rate |
| `feat_hist_win_rate_diff` | Home shrunk WC win rate − Away shrunk WC win rate |

---

## 4. Modeling Work

### 4.1 v1 — Baseline Multiclass (Elo)

**Notebook:** `multiclass/v1_baseline/multiclass_elo_model.ipynb`

**Task:** 3-class classification — `fav_wins` / `draw` / `fav_loses` from the perspective of the Elo-favoured team.

**Data:** 384 men's WC matches (2002–2022). Training: 2002–2014. Holdout: 2018 + 2022.

**Features:** 97 — historical stats, squad demographics, manager features, Elo gap.

**Models trained:** Logistic Regression, Random Forest, LightGBM, XGBoost (all 4 with defaults), then XGBoost tuned with Optuna (40 trials).

**Results:**

| Model | CV Macro-AUC | Holdout Macro-AUC | Holdout Macro-F1 |
|---|---|---|---|
| XGBoost (default) | 0.671 | — | 0.472 |
| XGBoost (Optuna-tuned) | **0.711** | **0.627** | **0.373** |

**Key findings:**
- Elo gap is the single strongest feature (highest mean |SHAP|)
- Historical win rates, squad experience, and manager track record contribute beyond Elo
- Draw prediction is weak across all models (recall < 0.10)
- ~0.084 CV→holdout AUC gap suggests structural ceiling, not just overfitting

---

### 4.2 Player Model v3

**Notebook:** `model/player_model_v3.ipynb`

**Task:** 3-class classification (win / draw / loss from home team perspective) using player-level club statistics.

**Data:** 238–314 matches (2006–2022) after merging with player club stats.

**Features (15, after VIF filtering):**
- Club strength by position (FW/MF/DF avg club Elo)
- Squad goals & assists per appearance (adjusted, Elo-weighted)
- GK clean sheet rate
- WC pedigree (historical finals, semis, wins)
- Defending champion flag
- Squad cohesion (same-club player pairs, largest club block)
- National team Elo

**Motivation for VIF filtering:** 5 features removed due to multicollinearity (VIF > 5): `mismatch_home_attack`, `diff_defensive_mv`, `diff_squad_goals_elo_wt`, and 2 others.

**Models trained:**

| Model | Avg Accuracy | Avg Macro-F1 | Notes |
|---|---|---|---|
| Elo-only (baseline) | **0.711** | **0.501** | Single feature |
| L1 Logistic Regression | 0.658 | 0.465 | 15 features — underperforms Elo |
| L1 + Draw Threshold | 0.615 | 0.530 | Better F1, worse accuracy |
| Elo-Residuals | 0.671 | 0.480 | Orthogonalise features vs Elo first |
| Elo-Adjustment | 0.671 | 0.476 | Feed Elo probs as meta-feature |

**Key findings:**
- Player club statistics (market value, goals, cohesion, pedigree) **do not beat Elo alone**
- Orthogonalising features against Elo recovers marginal signal but not enough to beat the baseline
- 2022 was particularly hard (log-loss jumps to ~1.0 across all models — Qatar tournament was anomalous)
- VIF filtering helped stability but the remaining features still added more noise than signal

---

### 4.3 v2 — Integrated Features

**Notebook:** `multiclass/v2_integration/03_model_training.ipynb`  
**Supporting:** `01_features_team.ipynb`, `02_features_player_squad.ipynb`, `04_interpretability.ipynb`

**Task:** 3-class classification (fav wins / draw / fav loses) with a 2×2 experimental design isolating the effect of *more samples* vs *more features*.

**Experimental configurations:**

| Config | Features | Training window | Train rows |
|---|---|---|---|
| Control | 47 (team only) | 2006–2014 | 192 |
| Treatment 1 | 47 (team only) | 1998–2014 | 320 |
| Treatment 2 | 110 (team + squad) | 2006–2014 | 192 |

Treatment 2 squad features (25 additional columns from `02_features_player_squad.ipynb`):
- Club Elo strength by position (`pl_FW/MF/DF_avg_strength`)
- Elo-weighted goal/assist volumes
- Squad cohesion (`sq_club_pairs`, `sq_largest_club_block`)
- WC pedigree (`sq_wc_finals`, `sq_wc_semis`, `sq_wc_appearances`)
- Defending champion flag

**Models trained:** Logistic Regression, Random Forest, LightGBM, XGBoost (all configs).

**Results:**

| Config | Best model | CV Macro-AUC | Holdout Macro-AUC | Holdout Accuracy |
|---|---|---|---|---|
| Control | Random Forest | 0.680 | **0.608** | 0.633 |
| Treatment 1 | Random Forest | **0.744** | **0.608** | **0.664** |
| Treatment 2 | XGBoost | 0.625 | 0.598 | 0.625 |

**Key findings:**
- **More training data** (treatment 1: 1998–2014) raised CV AUC from 0.680 → 0.744 but did *not* improve holdout
- **Adding squad features without selection** (treatment 2) hurt performance on both CV and holdout
- Structural ceiling around holdout macro-AUC = 0.608 across all 3-class configs
- Selected final model: Treatment 1 RF (team-only features, 1998–2014 window)

**Interpretability (04_interpretability.ipynb):**
- SHAP + LIME applied to the selected model
- Defending champion effect: `sq_defending_champion` showed negative SHAP — being the defending champion is slightly disadvantageous (pressure / opponents' preparation)
- Geographic bias: AFC and CONCACAF predictions less reliable than UEFA/CONMEBOL

---

### 4.4 Regression — Goal Difference

**Notebook:** `model/regression/goal_diff_model.ipynb`

**Task:** Regression — predict the *goal margin* (`goal_diff = fav_goals − und_goals`) as a continuous value. Fundamentally different from the classification notebooks.

**Data:** 244 training matches (2002–2014), 119 holdout matches (2018 + 2022). 21 penalty-shootout matches excluded (score stays level; shootout outcome cannot be captured by goal diff).

**Features:** Same 97 as v1 — historical stats, squad demographics, manager features, Elo gap.

**Models trained:** DummyRegressor (predict the mean) vs Ridge Regression (α tuned over [0.01 → 100] via GridSearchCV with LOGO-CV).

**Results:**

| Model | CV MAE | Holdout MAE | Holdout RMSE | Best α |
|---|---|---|---|---|
| Dummy (predict mean) | 1.103 | 1.127 | 1.521 | — |
| Ridge | 1.161 | 1.154 | **1.484** | 100 |

**Key findings:**
- Ridge barely outperforms predicting the mean (RMSE improvement of 0.037)
- Best α = 100 (very high regularisation) indicates the model collapses toward the mean anyway
- Goal margins are highly variable and low-signal — the task is fundamentally harder than win/loss prediction
- Architecture is in place for future extension: Elastic Net, Random Forest regressor, Poisson count models

---

### 4.5 v3 — Advanced Ensemble

**Notebook:** `multiclass/v3_ensemble/advanced_ensemble.ipynb`

**Task:** Binary classification — `y_win` (1 = home team wins, 0 = draw or away win).

**Data:** `class_a_squad_2006_2022.csv` — 313 matches × 183 features (2006–2022).

**CV strategy:** Leave-One-Tournament-Out (LOTO) — 5 folds, each fold holds out one complete World Cup year. No separate holdout; full data used via OOF predictions.

#### Step 1 — Feature Selection via SHAP

A quick LightGBM was trained on all 171 usable features (3 dropped for >50% missingness). SHAP values were computed to rank features by mean absolute importance. **Top 25 features selected.**

**Top 5 features by SHAP importance:**

| Rank | Feature | Group |
|---|---|---|
| 1 | `feat_elo_rating_diff` | Rankings |
| 2 | `home_squad_fwd_avg_assists` | Club performance |
| 3 | `home_squad_avg_appearances` | Club performance |
| 4 | `home_squad_gk_avg_clean_sheets` | Club performance |
| 5 | `home_squad_fwd_avg_minutes` | Club performance |

Note: 4 of the top 5 features are **squad club performance stats** — the new features added in this work.

#### Step 2 — LightGBM with Optuna Tuning

50 Optuna trials over key hyperparameters (`n_estimators`, `learning_rate`, `num_leaves`, `min_child_samples`, `subsample`, `colsample_bytree`, `reg_alpha`, `reg_lambda`), optimising LOTO-CV binary AUC.

Best hyperparameters found:

```
n_estimators:      125
learning_rate:     0.073
num_leaves:        33
min_child_samples: 17
subsample:         0.917
colsample_bytree:  0.665
reg_alpha:         0.0035
reg_lambda:        0.0094
```

#### Step 3 — Stacking Ensemble

Three base learners trained independently with LOTO-CV to generate out-of-fold (OOF) predictions:
- Logistic Regression (L2, C=0.1)
- Tuned LightGBM
- Ridge Classifier

OOF predictions stacked as meta-features → Logistic Regression meta-learner.

#### Results

| Model | OOF Accuracy | OOF AUC | OOF Log-Loss | Fold Acc μ ± σ |
|---|---|---|---|---|
| Logistic Regression (baseline) | 0.626 | 0.667 | 0.787 | 0.626 ± 0.042 |
| LightGBM (tuned) | **0.760** | **0.829** | 0.551 | 0.760 ± 0.051 |
| Stacking Ensemble | **0.760** | 0.813 | **0.526** | 0.760 ± 0.048 |

**Per-fold breakdown (LightGBM):**

| Year | N matches | Accuracy | AUC |
|---|---|---|---|
| 2006 | 62 | 0.742 | 0.832 |
| 2010 | 63 | 0.698 | 0.786 |
| 2014 | 64 | **0.828** | **0.915** |
| 2018 | 63 | 0.794 | 0.852 |
| 2022 | 61 | 0.738 | 0.770 |

**Key findings:**
- LightGBM with SHAP-selected features improved accuracy from 62.6% → **76.0%** vs LR baseline
- Stacking matches LightGBM on accuracy but has the best log-loss — most calibrated win probabilities
- 2022 remains the hardest tournament (lowest AUC 0.770) consistent with findings across all notebooks

---

## 5. Cross-Notebook Comparison

| Notebook | Task | Features | Best CV metric | Best holdout / OOF | Squad features helped? |
|---|---|---|---|---|---|
| v1 XGBoost (Optuna) | 3-class | 97 | 0.711 macro-AUC | 0.627 macro-AUC | N/A (not included) |
| player_model_v3 (Elo-only) | 3-class | 1 (Elo only) | 0.711 accuracy | — | No — hurt performance |
| v2 control (RF) | 3-class | 47 | 0.680 macro-AUC | 0.608 macro-AUC | N/A (not included) |
| v2 treatment1 (RF, more data) | 3-class | 47 | **0.744 macro-AUC** | 0.608 macro-AUC | N/A (not included) |
| v2 treatment2 (XGB + squad) | 3-class | 110 | 0.625 macro-AUC | 0.598 macro-AUC | ❌ Hurt performance |
| regression/goal_diff | Regression | 97 | — | 1.484 RMSE | N/A |
| **v3 LightGBM (tuned)** | **Binary** | **25** | **0.829 binary AUC** | **0.760 OOF acc** | **✅ Top 4/5 SHAP features** |
| **v3 Stacking Ensemble** | **Binary** | **25** | **0.813 binary AUC** | **0.760 OOF acc** | **✅ Best log-loss (0.526)** |

> ⚠️ **Metrics are not directly comparable across task types.** 3-class macro-AUC and binary AUC measure different things. Binary AUC is structurally higher because the task is simpler (draw and loss are merged into one class).

### Why v3 numbers are higher — and what that means

Three factors explain the apparent gap between v2 (0.608 AUC) and v3 (0.829 AUC):

**1. Simpler task (biggest factor)**
Binary (win / no-win) vs 3-class. All prior notebooks struggled most with draw prediction (recall consistently < 0.10). Merging draws into the negative class removes the hardest prediction problem entirely.

**2. Better squad features**
v2's squad features were Elo-weighted club prestige scores and cohesion counts. v3 uses positional *performance* stats — forward goals and assists per season, GK clean sheet rate, minutes played by position. These capture actual form, not just club reputation.

**3. SHAP-based feature selection**
v3 prunes 171 → 25 features before training. v2 treatment2 stacked 63 squad features on top of 47 team features with no pruning, adding noise that actively hurt performance. Feature selection was the missing step.

**The v2 finding ("squad features hurt") and v3 finding ("squad features help") are both valid** — they reflect different feature designs and different tasks, not a contradiction.

---

## 6. Key Findings

1. **Elo is the single strongest predictor** across every notebook. No model beats Elo alone in 3-class prediction, and Elo is the top SHAP feature in binary prediction too.

2. **Squad features can help — but only with the right design.** Prestige-based features (club Elo rank, market value) don't add signal. Performance-based features (actual goals, assists, clean sheets from last season) do — when selected via SHAP rather than added wholesale.

3. **3-class prediction has a structural ceiling around 0.608 holdout macro-AUC.** More training data (treatment1) did not break through. The limiting factor appears to be draw unpredictability, not model complexity.

4. **Binary prediction is more tractable.** Removing draw prediction as a class achieves 0.829 OOF AUC with the right model.

5. **Feature selection is critical on a small dataset.** With only 313 rows, going from 171 → 25 features via SHAP importance was essential to prevent overfitting.

6. **2022 (Qatar) is consistently the hardest tournament** to predict across all notebooks — lowest AUC, highest log-loss, most upsets. Likely due to the winter timing, unusual venues, and compressed schedule.

7. **Goal margin prediction is near-random.** Ridge regression barely beats predicting the mean (RMSE improvement of 0.037). Match-level goal differences are too noisy to model with the current features.

---

## 7. Open Questions

The following are unresolved questions worth addressing in the final report or future work:

- **Can SHAP-selected squad features help the 3-class task too?** Re-running v2 treatment2 with the 25 SHAP-selected features (instead of all 110) might close the gap with the team-only baseline.

- **Binary vs 3-class for the final deliverable?** If the team needs draw prediction for tournament simulation, binary framing is not sufficient. If the goal is win probability for bracket prediction, binary is the right choice.

- **Should 2022 be reserved as a final holdout?** v3 uses 2022 in training (via LOTO). Reserving it as a true holdout (matching v1/v2 protocol) would give a cleaner comparison.

- **Can the regression model be improved?** Poisson regression for individual team goal counts, or a hurdle model separating "0-0 draw" from "scoring game", might extract more signal than a single Ridge model on goal difference.

- **Tournament simulation.** Combining win probability (v3 binary) + expected goal margin (regression) could support a full bracket simulation. Neither notebook currently does this end-to-end.
