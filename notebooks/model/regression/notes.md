# This same note is at the top of the jupyter notebook as well

## Overview (with a few extension options)

* Regression vs. Classification:
  * **Pros**: regression uses the margin of victory, so a 3–0 and 1–0 are not treated as equally strong wins.
  * **Cons**: soccer scores are **low-count, discrete, noisy, and heavily concentrated near 0**, so plain regression is a bit less natural than classification.
* **Primary regression approach**: predict **goal difference**; *vs.* **Optional stronger extension**: predict the **two team scores separately** with count models, then derive win/draw/loss from those
* Symmetric vs. assymetric threshold

## Models

I used this following set:

1. **Ridge regression**
   Best baseline. Stable for small data, easy to interpret, good when sample size is limited.
2. **Elastic Net / Lasso**
   Useful if we have many correlated engineered features (we probably do because Tony and Oge work on feature engineering) and want some regularization / feature selection.
3. **Random Forest Regressor**
   Captures nonlinearity and interactions without much preprocessing.
4. **XGBoost Regressor**
   Probably the strongest nonlinear candidate, especially since Mingjie already uses XGBoost on the classification side.

That gives us a very nice comparison:

- linear regularized baseline
- sparse/regularized linear variant
- bagged tree model
- boosted tree model

## Evaluation

I used both **regression** metrics and **converted classification** metrics.

### Regression-side metrics

These tell whether the model predicts score margin well:

* **MAE** on goal difference
* **RMSE** on goal difference

I would make **MAE **the main one because soccer score margins are small and MAE is easier to interpret.

### Converted 3-class metrics

After applying threshold tt**t**, compare fairly to Mingjie's classification approach:

* **macro F1**
* **accuracy**
* confusion matrix
* optionally macro recall

This is crucial, because even if regression has decent MAE, it may still map poorly into draw/upset/win classes.

## Comparison with Mingjie's classifier

I used the **same split and same feature matrix entry point** (`fav_df`) and only changed:

* target $y$
* estimator type
* decision rule from continuous output to 3 classes

That makes the comparison clean:

* same preprocessing base
* same temporal split
* same evaluation period
* same engineered features

This is exactly in accordance with the project design of comparing modeling strategies on the same underlying data.

## Potential Weakness

- regression to score difference may under-predict draws

A continuous regressor tends to shrink predictions toward the mean. That can be okay, but it means:

* many predictions may cluster around small positive values
* the threshold may become the main determinant of draw frequency

That is not necessarily bad, but it means threshold tuning is extremely important.

## Better Alternative

### model each team's goals separately

Predict:

* favored goals
* underdog goals

with **Poisson regression** or another count model, then derive:

* predicted goal difference
* predicted class
* even draw probability

Why this is attractive:

* goals are nonnegative counts
* soccer score distributions are low-count
* draw probability emerges more naturally

This is more principled than plain regression on difference.
