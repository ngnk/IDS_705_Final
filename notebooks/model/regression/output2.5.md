Detected penalty-shootout column: penalty_shootout

Penalty-shootout flag distribution:
penalty_shootout
0    363
1     21
Name: count, dtype: int64

Shapes:
Before removing shootouts: (384, 194)
After removing shootouts : (363, 194)
Dropped rows: 21

Clean split summary:
Train size: 244
Holdout size: 119

Train goal_diff distribution:
goal_diff
-3     1
-2     7
-1    25
 0    48
 1    83
 2    45
 3    22
 4     9
 6     2
 7     1
 8     1
Name: count, dtype: int64

Holdout goal_diff distribution:
goal_diff
-2     2
-1    18
 0    19
 1    37
 2    26
 3    12
 4     1
 5     3
 7     1
Name: count, dtype: int64

Agreement after removing shootouts: 1.0

Top 20 missing-rate features after shootout filtering:
und_hist_pso_win_rate_shrunk                0.713115
feat_away_mgr_hist_win_rate_shrunk          0.700820
feat_home_mgr_hist_win_rate_shrunk          0.696721
fav_hist_pso_win_rate_shrunk                0.360656
fav_rest_days_since_prev_match              0.262295
und_rest_days_since_prev_match              0.262295
feat_rest_days_diff                         0.262295
feat_away_hist_win_rate_vs_home_conf        0.196721
feat_hist_goal_diff_per_match_diff          0.172131
und_squad_squad_jaccard_vs_prev_wc          0.143443
und_hist_goal_diff_per_match                0.143443
und_hist_frac_tournaments_reached_ko        0.143443
und_hist_et_rate                            0.143443
und_squad_squad_overlap_count_vs_prev_wc    0.143443
feat_home_hist_win_rate_vs_away_conf        0.114754
fav_hist_goal_diff_per_match                0.032787
fav_hist_frac_tournaments_reached_ko        0.032787
fav_squad_squad_overlap_count_vs_prev_wc    0.032787
fav_squad_squad_jaccard_vs_prev_wc          0.032787
fav_hist_et_rate                            0.032787
dtype: float64

Part 2.5 completed successfully.
