Train shape: (244, 97) (244,)
Holdout shape: (119, 97) (119,)
Training years: [np.int64(2002), np.int64(2006), np.int64(2010), np.int64(2014)]
Fitting 4 folds for each of 216 candidates, totalling 864 fits

Best RF params:
{'model__max_depth': None, 'model__max_features': 'sqrt', 'model__min_samples_leaf': 1, 'model__min_samples_split': 2, 'model__n_estimators': 200}
Best RF CV MAE: 1.1017016129032255

RandomForestRegressor LOTO CV results:
   fold val_year       mae      rmse  pred_mean  pred_std  pred_min  pred_max
0     1   [2002]  1.223306  1.654193   1.148306  0.313419     0.140     1.875
1     2   [2006]  1.075667  1.459102   0.861833  0.372008     0.015     1.535
2     3   [2010]  0.980000  1.400804   1.130161  0.419279     0.150     2.160
3     4   [2014]  1.127833  1.492295   1.101667  0.368024     0.270     2.280

RandomForestRegressor mean CV metrics:
mae     1.101702
rmse    1.501599
dtype: float64

RandomForestRegressor holdout metrics:
{'holdout_mae': 1.139747899159664, 'holdout_rmse': 1.470675543626754, 'pred_mean': 1.1207563025210086, 'pred_std': 0.3820360308227914, 'pred_min': 0.25, 'pred_max': 2.145, 'true_mean': 1.084033613445378, 'true_std': 1.52061371916202}

Model comparison:
                   model    cv_mae   cv_rmse  holdout_mae  holdout_rmse
0                  Ridge  1.160829  1.569069     1.153497      1.483703
1  RandomForestRegressor  1.101702  1.501599     1.139748      1.470676

Part 5 completed successfully.
