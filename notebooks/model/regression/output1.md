# 1. Load Raw Tables
Loaded raw tables:
matches: (1248, 28)
tournaments: (30, 17)
teams: (88, 11)
team_appearances: (2496, 17)
squads: (13843, 6)
players: (10401, 12)
elo_raw: (17200, 17)
# 2. Date Parsing + tournament Year Info
# 3. Base Match Table
base shape after match/team/stadium merge: (1248, 45)
# 4. Historical Team Features
base shape after historical team stats: (1248, 83)
# 5. Win Rate *vs.* Opponent Confederation
Added confederation matchup features.
# 6. Squad Features
base shape after squad features: (1248, 119)
# 7. Manager Features
base shape after manager features: (1248, 133)
# 8. Schedule/Context Features
base shape after schedule/context features: (1248, 137)
# 9. Build `df_all`
df_all shape: (1248, 104)
# 10. Restrict to Men's World Cups + Join ELO + Build `y3`
men shape after Elo join: (384, 109)
y3 distribution:
y3
0     63
1     67
2    254
Name: count, dtype: int64
# 11. Build `fav_df`
Done.
fav_df shape: (384, 186)
X_all shape: (384, 97)
Unique classes in y_all: [0 1 2]

First 20 columns of fav_df:
['match_id', 'tournament_id', 'year', 'home_team_id', 'away_team_id', 'y_win', 'away_hist_draws', 'away_hist_et_matches', 'away_hist_et_rate', 'away_hist_frac_tournaments_reached_ko', 'away_hist_goal_diff_per_match', 'away_hist_goal_diff_sum', 'away_hist_ko_matches', 'away_hist_ko_win_rate_shrunk', 'away_hist_ko_wins', 'away_hist_losses', 'away_hist_n_matches', 'away_hist_n_tournaments', 'away_hist_pso_matches', 'away_hist_pso_win_rate_shrunk']
