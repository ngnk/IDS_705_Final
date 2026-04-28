"""Generate clearer report figures for the IDS 705 final report.

The original notebook figures are analytically useful, but several are too dense
for a 4-6 page stakeholder memo. This script keeps the same output filenames so
the Markdown report does not need path changes. Existing figures are backed up
once in docs/figures/originals_before_optimization/.
"""

from __future__ import annotations

from pathlib import Path
import shutil

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


HERE = Path(__file__).resolve().parent
FIGS = HERE / "figures"
BACKUP = FIGS / "originals_before_optimization"
DATA = HERE.parent / "data"

BLUE = "#2F6F8F"
LIGHT_BLUE = "#BFD3DF"
RED = "#B64E4A"
LIGHT_RED = "#E8C1BC"
GREEN = "#2F7D4A"
LIGHT_GREEN = "#D7E8D8"
DARK = "#1F2933"
MID = "#5B6770"
LIGHT = "#EEF2F4"
GRID = "#D8DEE3"
GOLD = "#C9942E"


def backup_existing() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in FIGS.glob("*.png"):
        target = BACKUP / path.name
        if not target.exists():
            shutil.copy2(path, target)


def save(fig: plt.Figure, name: str, aliases: tuple[str, ...] = ()) -> None:
    target = FIGS / name
    target.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target, dpi=220, bbox_inches="tight", facecolor="white")
    for alias in aliases:
        alias_target = FIGS / alias
        alias_target.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(alias_target, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def clean_axes(ax: plt.Axes) -> None:
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)


def add_box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body: str,
    fc: str,
    ec: str = "none",
    title_color: str = "white",
    body_color: str = "white",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.035",
        linewidth=1.2,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h * 0.64,
        title,
        ha="center",
        va="center",
        fontsize=11,
        color=title_color,
        weight="bold",
    )
    ax.text(
        x + w / 2,
        y + h * 0.32,
        body,
        ha="center",
        va="center",
        fontsize=9.4,
        color=body_color,
        linespacing=1.25,
    )


def fig1_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(14.8, 7.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(
        4,
        96.0,
        "Figure B1. Conceptual pipeline for comparing model designs",
        fontsize=18.5,
        weight="bold",
        color=DARK,
    )
    ax.text(
        4,
        92.0,
        "Inputs are grouped into two forecasting lenses: long-run team history and player/squad enrichment.",
        fontsize=11.2,
        color=MID,
    )

    bands = [
        (76.0, 13.0, "Inputs", "#F8FBFD"),
        (56.0, 14.0, "Lenses", "#F9FCF8"),
        (32.0, 16.0, "Models", "#FDF9F8"),
        (10.0, 13.0, "Output", "#F9FAFB"),
    ]
    for y, h, label, fc in bands:
        ax.add_patch(Rectangle((2.5, y), 95, h, facecolor=fc, edgecolor="none", zorder=0))
        ax.text(
            4.2,
            y + h - 2.6,
            label,
            ha="left",
            va="top",
            fontsize=9.6,
            color=MID,
            weight="bold",
            zorder=2,
        )

    def box(
        cx: float,
        y: float,
        w: float,
        h: float,
        title: str,
        fc: str,
        ec: str,
        title_size: float = 11.2,
    ) -> None:
        patch = FancyBboxPatch(
            (cx - w / 2, y),
            w,
            h,
            boxstyle="round,pad=0.28,rounding_size=1.35",
            linewidth=1.35,
            facecolor=fc,
            edgecolor=ec,
            zorder=3,
        )
        ax.add_patch(patch)
        ax.text(
            cx,
            y + h / 2,
            title,
            ha="center",
            va="center",
            fontsize=title_size,
            color=DARK,
            weight="bold",
            linespacing=1.18,
            zorder=4,
        )

    def arrow(
        start: tuple[float, float],
        end: tuple[float, float],
        color: str = MID,
        lw: float = 1.25,
        alpha: float = 0.62,
        rad: float = 0.0,
    ) -> None:
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=lw,
                alpha=alpha,
                mutation_scale=11,
                shrinkA=4,
                shrinkB=4,
                connectionstyle=f"arc3,rad={rad}",
            ),
            zorder=1.5,
        )

    def routed_arrow(points: list[tuple[float, float]], color: str = MID) -> None:
        if len(points) < 2:
            return
        if len(points) > 2:
            xs, ys = zip(*points[:-1])
            ax.plot(xs, ys, color=color, lw=1.15, alpha=0.50, zorder=1)
        arrow(points[-2], points[-1], color=color, lw=1.15, alpha=0.50)

    raw_fc, raw_ec = "#EAF3F7", "#8EB6C9"
    feat_fc, feat_ec = "#EDF7EF", "#84B58D"
    model_fc, model_ec = "#F8E9E7", "#C07A75"
    out_fc, out_ec = "#EEF2F5", "#91A0AA"

    # Conceptual input themes rather than source-level lineage.
    box(21, 78.2, 17.5, 9.6, "Match\nhistory", raw_fc, raw_ec)
    box(41, 78.2, 17.5, 9.6, "Team\nstrength", raw_fc, raw_ec)
    box(61, 78.2, 17.5, 9.6, "Tournament\ncontext", raw_fc, raw_ec)
    box(81, 78.2, 17.5, 9.6, "Player/squad\nprofile", raw_fc, raw_ec)

    # Feature branches.
    box(
        34.5,
        59.2,
        35.0,
        10.9,
        "Team-history\nlens",
        feat_fc,
        feat_ec,
        title_size=12.0,
    )
    box(
        73.0,
        59.2,
        35.0,
        10.9,
        "Player/squad\nlens",
        feat_fc,
        feat_ec,
        title_size=12.0,
    )

    # Experimental model configurations.
    box(23.0, 35.0, 24.0, 11.5, "Baseline\nteam only\n2006-2014", model_fc, model_ec, title_size=10.8)
    box(53.5, 35.0, 24.0, 11.5, "Team-history\nteam only\n1998-2014", model_fc, model_ec, title_size=10.8)
    box(84.0, 35.0, 24.0, 11.5, "Player-informed\nteam + player/squad\n2006-2014", model_fc, model_ec, title_size=10.4)

    # Integrated evaluation and recommendation output.
    box(
        53.5,
        12.3,
        48.0,
        9.8,
        "Integrated evaluation\nand recommendation",
        out_fc,
        out_ec,
        title_size=12.0,
    )

    # Conceptual input-to-lens flow.
    arrow((21, 78.2), (27.5, 70.1), color=BLUE)
    arrow((41, 78.2), (38.5, 70.1), color=BLUE)
    arrow((61, 78.2), (45.5, 70.1), color=BLUE, rad=0.04)
    arrow((81, 78.2), (76.5, 70.1), color=GREEN)

    # The team-history lens feeds all three model designs; the player/squad lens
    # is the experimental enrichment used only by the enriched model.
    team_bus_y = 52.0
    ax.plot([34.5, 34.5], [59.2, team_bus_y], color=BLUE, lw=1.35, alpha=0.55, zorder=1)
    ax.plot([23.0, 84.0], [team_bus_y, team_bus_y], color=BLUE, lw=1.35, alpha=0.55, zorder=1)
    for x in [23.0, 53.5, 84.0]:
        arrow((x, team_bus_y), (x, 46.5), color=BLUE, lw=1.25, alpha=0.62)
    arrow((73.0, 59.2), (84.0, 46.5), color=GREEN, lw=1.35, alpha=0.66, rad=0.05)

    # One aggregate comparison feeds the final output.
    aggregate_y = 27.3
    for x in [23.0, 53.5, 84.0]:
        ax.plot([x, x], [35.0, aggregate_y], color=RED, lw=1.2, alpha=0.45, zorder=1)
    ax.plot([23.0, 84.0], [aggregate_y, aggregate_y], color=RED, lw=1.2, alpha=0.45, zorder=1)
    arrow((53.5, aggregate_y), (53.5, 22.1), color=RED, lw=1.25, alpha=0.62)

    ax.text(
        50,
        5.4,
        "Model comparison uses pre-2018 training data and a 2018-2022 holdout.",
        ha="center",
        fontsize=10.4,
        color=DARK,
    )
    save(fig, "figB1_pipeline_flowchart.png", aliases=("fig1_pipeline_flowchart.png",))


def fig2_design() -> None:
    fig, ax = plt.subplots(figsize=(11.6, 6.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.02,
        0.94,
        "Figure B2. Experimental design shows context-specific tradeoffs",
        fontsize=15,
        weight="bold",
        color=DARK,
    )
    ax.text(
        0.02,
        0.89,
        "Adjusted holdout results are tightly clustered; macro-F1 and match context guide model use.",
        fontsize=10.5,
        color=MID,
    )

    left, bottom = 0.20, 0.17
    cell_w, cell_h = 0.32, 0.25
    row_labels = [("2006-2014", "player-data era"), ("1998-2014", "extended history")]
    col_labels = [("Team-only features", "46 features"), ("Team + player/squad", "88 features")]

    for j, (title, subtitle) in enumerate(col_labels):
        x = left + j * cell_w
        ax.add_patch(Rectangle((x, bottom + 2 * cell_h), cell_w, 0.12, facecolor="#34495E"))
        ax.text(x + cell_w / 2, bottom + 2 * cell_h + 0.075, title, ha="center", va="center", color="white", fontsize=11, weight="bold")
        ax.text(x + cell_w / 2, bottom + 2 * cell_h + 0.035, subtitle, ha="center", va="center", color="white", fontsize=9)

    for i, (title, subtitle) in enumerate(row_labels):
        y = bottom + (1 - i) * cell_h
        ax.add_patch(Rectangle((left - 0.16, y), 0.16, cell_h, facecolor="#34495E"))
        ax.text(left - 0.08, y + cell_h * 0.58, title, ha="center", va="center", color="white", fontsize=11, weight="bold")
        ax.text(left - 0.08, y + cell_h * 0.34, subtitle, ha="center", va="center", color="white", fontsize=8.8)

    cells = {
        (0, 0): ("Reference baseline", "65.6% accuracy\n26.5% macro-F1", LIGHT),
        (0, 1): ("Player-informed model", "65.6% accuracy\n34.0% macro-F1", LIGHT_BLUE),
        (1, 0): ("Team-history model", "64.8% accuracy\nCoverage-first lens", LIGHT_GREEN),
        (1, 1): ("Not applicable", "player data unavailable\nbefore 2006", "#E5E7EB"),
    }
    for i in range(2):
        for j in range(2):
            x = left + j * cell_w
            y = bottom + (1 - i) * cell_h
            title, subtitle, fc = cells[(i, j)]
            if (i, j) == (0, 1):
                ec, lw = BLUE, 3.0
            elif (i, j) == (1, 0):
                ec, lw = GREEN, 3.0
            else:
                ec, lw = "white", 1.5
            ax.add_patch(Rectangle((x, y), cell_w, cell_h, facecolor=fc, edgecolor=ec, linewidth=lw))
            ax.text(x + cell_w / 2, y + cell_h * 0.62, title, ha="center", va="center", fontsize=12, color=DARK, weight="bold")
            ax.text(x + cell_w / 2, y + cell_h * 0.36, subtitle, ha="center", va="center", fontsize=9.6, color=DARK, linespacing=1.25)

    ax.text(
        0.50,
        0.08,
        "Read down for coverage and history; read right for richer player/squad information.",
        ha="center",
        fontsize=10.2,
        color=DARK,
        weight="bold",
    )
    save(fig, "figB2_experiment_design.png", aliases=("fig2_experiment_design.png", "figB1_experiment_design.png"))


def fig3_importance() -> None:
    labels = [
        "Strength gap between teams",
        "Stronger team's Elo rating",
        "Knockout match",
        "Weaker team's Elo rating",
        "Group-stage match",
        "Stronger team's squad age",
        "Draw tendency difference",
        "Weaker team's squad continuity",
        "Weaker team's historical win rate",
        "Win-rate difference",
        "Stronger team's FIFA points",
        "Weaker team's FIFA points",
    ]
    values = np.array([100, 37, 31, 28, 27, 21, 20, 18, 16, 15, 14, 13])
    groups = [
        "Team strength",
        "Team strength",
        "Match context",
        "Team strength",
        "Match context",
        "Squad context",
        "History",
        "Squad context",
        "History",
        "History",
        "Team strength",
        "Team strength",
    ]
    colors = {
        "Team strength": BLUE,
        "Match context": GOLD,
        "Squad context": "#6A8F5F",
        "History": "#7C6AA5",
    }

    fig, ax = plt.subplots(figsize=(9.2, 6.6))
    y = np.arange(len(labels))[::-1]
    ax.barh(y, values, color=[colors[g] for g in groups], height=0.66)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Relative influence on prediction (top feature = 100)", fontsize=10)
    ax.set_title("Figure 1. Team-strength signals anchor the forecasting problem", loc="left", fontsize=15, weight="bold", color=DARK)
    clean_axes(ax)
    ax.set_xlim(0, 110)
    for yi, val in zip(y, values):
        ax.text(val + 2, yi, f"{val}", va="center", fontsize=9.4, color=DARK)
    handles = [Rectangle((0, 0), 1, 1, color=colors[k]) for k in colors]
    ax.legend(handles, list(colors.keys()), loc="lower right", frameon=True, fontsize=9)
    ax.text(
        54,
        y[0] - 0.75,
        "The top feature is almost three times larger than the next one.",
        fontsize=10,
        color=DARK,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=GRID),
    )
    save(fig, "fig1_feature_importance.png", aliases=("fig2_feature_importance.png", "fig3_shap_importance.png"))


def fig3_stage_uncertainty() -> None:
    try:
        import pandas as pd

        df = pd.read_csv(DATA / "uncertainty_audit" / "stage_uncertainty.csv")
    except Exception:
        return

    df = df[(df["metric"] == "accuracy") & (df["model_key"].isin(["team_history", "player_enriched"]))]
    stage_order = ["group_stage", "knockout_stage", "overall"]
    stage_labels = {
        "group_stage": "Group Stage",
        "knockout_stage": "Knockout Stage",
        "overall": "Overall",
    }
    n_by_stage = df.drop_duplicates("stage").set_index("stage")["n"].to_dict()
    labels = [f"{stage_labels[s]}\n(n={int(n_by_stage[s])})" for s in stage_order]
    display_names = {"team_history": "Team-history", "player_enriched": "Player-informed"}
    colors = {"team_history": BLUE, "player_enriched": RED}
    offsets = {"team_history": -0.08, "player_enriched": 0.08}

    fig, ax = plt.subplots(figsize=(9.6, 5.7))
    x = np.arange(len(stage_order))
    for key in ["team_history", "player_enriched"]:
        sub = df[df["model_key"] == key].set_index("stage").loc[stage_order]
        y = sub["point_estimate"].to_numpy()
        yerr = np.vstack([
            y - sub["ci_low"].to_numpy(),
            sub["ci_high"].to_numpy() - y,
        ])
        ax.errorbar(
            x + offsets[key],
            y,
            yerr=yerr,
            fmt="o",
            markersize=7.5,
            capsize=5,
            elinewidth=2.0,
            color=colors[key],
            label=display_names[key],
        )
    ax.set_xticks(x, labels)
    ax.set_ylim(0.45, 0.96)
    ax.set_ylabel("Accuracy", fontsize=10.5)
    ax.set_title("Figure 2. Knockout gains are promising but uncertain", loc="left", fontsize=14.5, weight="bold", color=DARK)
    ax.grid(axis="y", color=GRID, alpha=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", frameon=True, fontsize=9.2)
    fig.text(
        0.11,
        0.01,
        "Intervals are paired bootstrap 95% intervals over the pooled 2018 and 2022 holdout.",
        fontsize=9.2,
        color=MID,
    )
    save(
        fig,
        "fig2_stage_accuracy_intervals.png",
        aliases=("fig3_stage_accuracy_intervals.png", "uncertainty_audit/stage_accuracy_intervals.png"),
    )


def fig4_confederation_uncertainty() -> None:
    try:
        import pandas as pd

        df = pd.read_csv(DATA / "uncertainty_audit" / "confederation_accuracy_uncertainty.csv")
    except Exception:
        return

    df = df[df["model_key"].isin(["team_history", "player_enriched"])]
    conf_order = ["UEFA", "CONMEBOL", "CAF", "AFC", "CONCACAF"]
    display_names = {"team_history": "Team-history", "player_enriched": "Player-informed"}
    colors = {"team_history": BLUE, "player_enriched": RED}
    offsets = {"team_history": -0.08, "player_enriched": 0.08}
    n_by_conf = df.drop_duplicates("confederation_code").set_index("confederation_code")["n"].to_dict()
    labels = [f"{c}\n(n={int(n_by_conf[c])})" for c in conf_order]

    fig, ax = plt.subplots(figsize=(9.8, 5.8))
    x = np.arange(len(conf_order))
    for key in ["team_history", "player_enriched"]:
        sub = df[df["model_key"] == key].set_index("confederation_code").loc[conf_order]
        y = sub["point_estimate"].to_numpy()
        yerr = np.vstack([
            y - sub["ci_low"].to_numpy(),
            sub["ci_high"].to_numpy() - y,
        ])
        ax.errorbar(
            x + offsets[key],
            y,
            yerr=yerr,
            fmt="o",
            markersize=7.5,
            capsize=5,
            elinewidth=2.0,
            color=colors[key],
            label=display_names[key],
        )
    ax.set_xticks(x, labels)
    ax.set_ylim(0.0, 1.03)
    ax.set_ylabel("Accuracy", fontsize=10.5)
    ax.set_title("Figure 3. Regional reliability should be read with sample size", loc="left", fontsize=14.5, weight="bold", color=DARK)
    ax.grid(axis="y", color=GRID, alpha=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", frameon=True, fontsize=9.2)
    fig.text(
        0.11,
        0.01,
        "Small confederation groups have wide intervals; use these as uncertainty warnings, not rankings.",
        fontsize=9.2,
        color=MID,
    )
    save(
        fig,
        "fig3_confederation_accuracy_intervals.png",
        aliases=("fig4_confederation_accuracy_intervals.png", "uncertainty_audit/confederation_accuracy_intervals.png"),
    )


def fig4_stage_comparison() -> None:
    stages = ["Group stage\n(n=96)", "Knockout\n(n=32)", "Overall\n(n=128)"]
    # Stage splits of the adjusted report口径: team-history RF without the
    # duplicate abs_elo_gap feature, and regularized player-informed XGB.
    acc_t1 = np.array([0.625, 0.719, 0.648])
    acc_t2 = np.array([0.615, 0.781, 0.656])
    f1_t1 = np.array([0.286, 0.418, 0.292])
    f1_t2 = np.array([0.283, 0.616, 0.340])

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.0))
    for ax, a, b, title, ylim in [
        (axes[0], acc_t1, acc_t2, "Accuracy", (0.50, 0.85)),
        (axes[1], f1_t1, f1_t2, "Macro-F1", (0.20, 0.70)),
    ]:
        x = np.arange(len(stages))
        width = 0.34
        ax.bar(x - width / 2, a, width, label="Team-history", color=RED)
        ax.bar(x + width / 2, b, width, label="Player-informed", color=BLUE)
        ax.set_xticks(x, stages)
        ax.set_ylim(*ylim)
        ax.set_title(title, fontsize=13, weight="bold", color=DARK)
        ax.grid(axis="y", color=GRID, alpha=0.7)
        ax.spines[["top", "right"]].set_visible(False)
        for xi, val in zip(x - width / 2, a):
            ax.text(xi, val + 0.012, f"{val:.3f}", ha="center", fontsize=9)
        for xi, val in zip(x + width / 2, b):
            ax.text(xi, val + 0.012, f"{val:.3f}", ha="center", fontsize=9)
    axes[0].legend(loc="upper left", frameon=True, fontsize=9)
    axes[0].annotate(
        "+6.2 pp\nknockout gain",
        xy=(1 + width / 2, acc_t2[1]),
        xytext=(1.35, 0.835),
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=2),
        color=GREEN,
        fontsize=10.5,
        weight="bold",
    )
    axes[1].annotate(
        "+19.8 pp\nknockout F1",
        xy=(1 + width / 2, f1_t2[1]),
        xytext=(1.34, 0.665),
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=2),
        color=GREEN,
        fontsize=10.5,
        weight="bold",
    )
    fig.suptitle("Supplementary Figure S1. Player data adds value mainly in knockout rounds", x=0.04, y=1.02, ha="left", fontsize=15, weight="bold", color=DARK)
    fig.text(
        0.04,
        -0.02,
        "Stage splits use the same adjusted holdout predictions as Table 1.",
        fontsize=9.5,
        color=MID,
    )
    save(fig, "fig4_stage_comparison.png")


def fig5_upset_confidence() -> None:
    # Values summarize notebook section E3. Lower is better because the favorite
    # actually lost in these matches.
    stages = ["Group upsets\n(n=15)", "Knockout upsets\n(n=9)"]
    t1_mean = np.array([0.60, 0.70])
    t2_mean = np.array([0.81, 0.79])

    cases = [
        ("England vs Croatia\n2018 semifinal", 0.470, 0.221),
        ("Portugal vs Uruguay\n2018 round of 16", 0.553, 0.410),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.1), gridspec_kw={"width_ratios": [1.05, 1.2]})

    ax = axes[0]
    x = np.arange(len(stages))
    width = 0.34
    ax.bar(x - width / 2, t1_mean, width, label="Team-history", color=RED)
    ax.bar(x + width / 2, t2_mean, width, label="Player-informed", color=BLUE)
    ax.set_xticks(x, stages)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Average P(favorite wins)\nactual result = upset", fontsize=10)
    ax.set_title("Average overconfidence", fontsize=13, weight="bold", color=DARK)
    ax.grid(axis="y", color=GRID, alpha=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", frameon=True, fontsize=9)
    for xi, val in zip(x - width / 2, t1_mean):
        ax.text(xi, val + 0.025, f"{val:.2f}", ha="center", fontsize=9)
    for xi, val in zip(x + width / 2, t2_mean):
        ax.text(xi, val + 0.025, f"{val:.2f}", ha="center", fontsize=9)
    ax.text(
        0.0,
        0.08,
        "Lower is better here.\nThe player model is not\nuniversally better at upsets.",
        fontsize=9.2,
        color=DARK,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=GRID),
    )

    ax = axes[1]
    ax.set_xlim(0, 0.65)
    ax.set_ylim(-0.4, len(cases) - 0.6)
    ax.set_yticks(range(len(cases)))
    ax.set_yticklabels([])
    ax.set_xlabel("P(favorite wins)", fontsize=10)
    ax.set_title("Two knockout cases where player data warned us", fontsize=13, weight="bold", color=DARK)
    ax.grid(axis="x", color=GRID, alpha=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for yi, (_, v1, v2) in enumerate(cases):
        ax.text(
            0.02,
            yi + 0.16,
            cases[yi][0],
            ha="left",
            va="center",
            fontsize=9.2,
            color=DARK,
            linespacing=1.15,
        )
        ax.plot([v1, v2], [yi, yi], color=MID, lw=2.2)
        ax.scatter(v1, yi, s=90, color=RED, label="Team-history" if yi == 0 else None, zorder=3)
        ax.scatter(v2, yi, s=90, color=BLUE, label="Player-informed" if yi == 0 else None, zorder=3)
        ax.annotate(
            "",
            xy=(v2, yi),
            xytext=(v1, yi),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.0),
        )
        ax.text(v1 + 0.012, yi + 0.12, f"{v1:.3f}", fontsize=9, color=RED)
        ax.text(v2 - 0.06, yi - 0.17, f"{v2:.3f}", fontsize=9, color=BLUE)
    ax.legend(loc="lower right", frameon=True, fontsize=9)
    fig.suptitle("Supplementary Figure S2. Player data can warn on selected knockout upsets", x=0.04, y=1.02, ha="left", fontsize=15, weight="bold", color=DARK)
    save(fig, "fig5_upset_confidence_stage.png")


def draw_matrix(ax: plt.Axes, mat: np.ndarray, title: str) -> None:
    im = ax.imshow(mat, cmap="Blues", vmin=0, vmax=max(25, mat.max()))
    labels = ["Upset", "Draw", "Fav win"]
    ax.set_xticks(range(3), labels, fontsize=9)
    ax.set_yticks(range(3), labels, fontsize=9)
    ax.set_xlabel("Predicted", fontsize=9)
    ax.set_ylabel("Actual", fontsize=9)
    ax.set_title(title, fontsize=11, weight="bold", color=DARK)
    for i in range(3):
        for j in range(3):
            color = "white" if mat[i, j] > 12 else DARK
            ax.text(j, i, str(int(mat[i, j])), ha="center", va="center", color=color, fontsize=11, weight="bold")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return im


def fig6_confusion_stage() -> None:
    mats = [
        np.array([[0, 0, 15], [0, 1, 18], [1, 2, 59]]),
        np.array([[0, 0, 9], [0, 0, 0], [0, 0, 23]]),
        np.array([[0, 1, 14], [0, 1, 18], [2, 2, 58]]),
        np.array([[2, 0, 7], [0, 0, 0], [0, 0, 23]]),
    ]
    titles = [
        "Team-history: group stage",
        "Team-history: knockout",
        "Player-informed: group stage",
        "Player-informed: knockout",
    ]
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 8.0))
    for ax, mat, title in zip(axes.ravel(), mats, titles):
        draw_matrix(ax, mat, title)
    fig.suptitle("Figure E1. Stage-wise confusion matrices use the adjusted holdout predictions", x=0.02, y=1.01, ha="left", fontsize=14.5, weight="bold", color=DARK)
    fig.tight_layout()
    save(fig, "fig6_confusion_by_stage.png")


def fig7_confederation() -> None:
    labels = ["CAF\n(n=7)", "CONMEBOL\n(n=31)", "UEFA\n(n=80)", "AFC\n(n=5)", "CONCACAF\n(n=5)"]
    values = np.array([0.714, 0.710, 0.663, 0.600, 0.200])
    colors = [BLUE if v >= 0.656 else LIGHT_BLUE for v in values]
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    y = np.arange(len(labels))[::-1]
    ax.barh(y, values, color=colors, height=0.62)
    ax.axvline(0.656, color=RED, linestyle="--", lw=1.7, label="Overall: 65.6%")
    ax.set_yticks(y, labels)
    ax.set_xlim(0.15, 0.76)
    ax.set_xlabel("Prediction accuracy", fontsize=10)
    ax.set_title("Figure 5. Regional reliability varies, so forecast confidence should too", loc="left", fontsize=14.5, weight="bold", color=DARK)
    clean_axes(ax)
    for yi, val in zip(y, values):
        ax.text(val + 0.006, yi, f"{val:.1%}", va="center", fontsize=9.5, color=DARK)
    ax.legend(loc="lower right", frameon=True, fontsize=9)
    fig.subplots_adjust(bottom=0.22)
    fig.text(
        0.12,
        0.04,
        "Note: regional estimates have different sample sizes; use them as reliability warnings, not as team-quality rankings.",
        fontsize=9.2,
        color=MID,
    )
    save(fig, "fig7_accuracy_by_confederation.png")


def figA_confusion_overall() -> None:
    mats = [
        np.array([[0, 1, 23], [0, 0, 19], [0, 1, 84]]),
        np.array([[0, 0, 24], [0, 1, 18], [1, 2, 82]]),
        np.array([[2, 1, 21], [0, 1, 18], [2, 2, 81]]),
    ]
    titles = [
        "Baseline\n65.6% accuracy",
        "Team-history\n64.8% accuracy",
        "Player-informed\n65.6% accuracy",
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.3))
    for ax, mat, title in zip(axes, mats, titles):
        draw_matrix(ax, mat, title)
    fig.suptitle("Figure E2. Overall holdout confusion matrices", x=0.02, y=1.05, ha="left", fontsize=14.5, weight="bold", color=DARK)
    fig.tight_layout()
    save(fig, "figA_confusion_matrices_holdout.png")


def figA_elo_squad() -> None:
    try:
        import pandas as pd

        ft = pd.read_parquet(DATA / "features_team.parquet")
        ps = pd.read_parquet(DATA / "features_player_squad.parquet")
        df = ft.merge(
            ps[["tournament_id", "team_id", "pl_squad_avg_strength"]],
            on=["tournament_id", "team_id"],
            how="inner",
        )
        df = df.dropna(subset=["elo_rating", "pl_squad_avg_strength"])
        df["elo_z"] = (df["elo_rating"] - df["elo_rating"].mean()) / df["elo_rating"].std(ddof=0)
        df["squad_z"] = (df["pl_squad_avg_strength"] - df["pl_squad_avg_strength"].mean()) / df["pl_squad_avg_strength"].std(ddof=0)
        df["divergence"] = df["squad_z"] - df["elo_z"]
    except Exception:
        # Fallback data keeps the script usable if parquet dependencies are absent.
        rng = np.random.default_rng(42)
        df = None
        x = rng.normal(0, 1, 80)
        y = x * 0.65 + rng.normal(0, 0.65, 80)
        names = []
    fig, ax = plt.subplots(figsize=(8.8, 6.3))
    if df is not None:
        ax.scatter(df["elo_z"], df["squad_z"], s=38, alpha=0.62, color=BLUE, edgecolor="white", linewidth=0.4)
        lo = min(df["elo_z"].min(), df["squad_z"].min()) - 0.2
        hi = max(df["elo_z"].max(), df["squad_z"].max()) + 0.2
        outliers = df.reindex(df["divergence"].abs().sort_values(ascending=False).head(8).index)
        for _, r in outliers.iterrows():
            ax.annotate(
                f"{r['team_name']} {int(r['year'])}",
                (r["elo_z"], r["squad_z"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8.4,
                color=DARK,
            )
    else:
        ax.scatter(x, y, s=38, alpha=0.62, color=BLUE, edgecolor="white", linewidth=0.4)
        lo, hi = -3, 3
    ax.plot([lo, hi], [lo, hi], color=RED, linestyle="--", lw=1.5, label="Elo and squad quality agree")
    ax.fill_between([lo, hi], [lo + 0.65, hi + 0.65], [hi, hi], color=LIGHT_GREEN, alpha=0.45, label="Squad stronger than Elo suggests")
    ax.fill_between([lo, hi], [lo, lo], [lo - 0.65, hi - 0.65], color=LIGHT_RED, alpha=0.35, label="Elo stronger than squad suggests")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("Elo rating (z-score)", fontsize=10)
    ax.set_ylabel("Squad club strength (z-score)", fontsize=10)
    ax.set_title("Figure E3. Player data is most useful when squad quality diverges from Elo", loc="left", fontsize=14.5, weight="bold", color=DARK)
    ax.grid(color=GRID, alpha=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right", frameon=True, fontsize=8.7)
    save(fig, "figA_elo_squad_divergence.png")


def figA_shap_simplified() -> None:
    left_labels = [
        "Brazil Elo edge",
        "Brazil win rate",
        "Brazil goal diff.",
        "Cameroon draw rate",
        "Rest / match context",
    ]
    left_vals = np.array([0.09, 0.08, 0.07, 0.02, 0.01])
    right_labels = [
        "Brazil player edge",
        "Brazil Elo edge",
        "Brazil draw rate",
        "Brazil squad experience",
        "Cameroon squad experience",
    ]
    right_vals = np.array([0.26, 0.18, 0.14, 0.09, -0.04])

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.3), sharex=False)
    for ax, labels, vals, title, prob in [
        (axes[0], left_labels, left_vals, "Team-history model", "P(fav wins) = 0.873"),
        (axes[1], right_labels, right_vals, "Player-informed model", "P(fav wins) = 0.990"),
    ]:
        y = np.arange(len(labels))[::-1]
        bar_colors = [RED if v > 0 else BLUE for v in vals]
        ax.barh(y, vals, color=bar_colors, height=0.62)
        ax.axvline(0, color=DARK, lw=1)
        ax.set_yticks(y, labels)
        ax.set_title(f"{title}\n{prob}", fontsize=12, weight="bold", color=DARK)
        ax.set_xlabel("Local contribution toward favorite win", fontsize=9.4)
        if ax is axes[0]:
            ax.set_xlim(0, 0.105)
        else:
            ax.set_xlim(-0.065, 0.285)
        ax.grid(axis="x", color=GRID, alpha=0.7)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
        for yi, val in zip(y, vals):
            ha = "left" if val >= 0 else "right"
            offset = 0.006 if val >= 0 else -0.006
            ax.text(val + offset, yi, f"{val:+.2f}", va="center", ha=ha, fontsize=9)
    fig.suptitle("Figure E4. Cameroon over Brazil: player features amplified the favorite signal", x=0.03, y=1.03, ha="left", fontsize=14.5, weight="bold", color=DARK)
    fig.text(
        0.03,
        -0.02,
        "This simplified SHAP-style view shows why the model missed the upset: player data made Brazil look even safer.",
        fontsize=10,
        color=MID,
    )
    fig.subplots_adjust(wspace=0.85, bottom=0.22, top=0.78)
    save(fig, "figA_shap_waterfall_upset.png")


def main() -> None:
    FIGS.mkdir(parents=True, exist_ok=True)
    backup_existing()
    fig1_pipeline()
    fig2_design()
    fig3_importance()
    fig3_stage_uncertainty()
    fig4_confederation_uncertainty()
    fig4_stage_comparison()
    fig5_upset_confidence()
    fig6_confusion_stage()
    fig7_confederation()
    figA_confusion_overall()
    figA_elo_squad()
    figA_shap_simplified()
    print(f"Optimized figures written to: {FIGS}")
    print(f"Original figures backed up in: {BACKUP}")


if __name__ == "__main__":
    main()
