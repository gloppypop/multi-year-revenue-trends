# src/viz.py
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def _save(fig, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=220)
    plt.close(fig)


def plot_total_revenue(
    monthly_total: pd.DataFrame,
    out_dir: str | Path,
    takeover_date: str = "2023-07-01",
) -> None:
    import numpy as np

    out_dir = Path(out_dir)
    df = monthly_total.copy()
    takeover_ts = pd.to_datetime(takeover_date)

    # Ensure sorted and datetime
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(11, 5))

    # Main line
    sns.lineplot(data=df, x="month", y="revenue", marker="o", linewidth=2, ax=ax)

    ax.set_title("Monthly Revenue (All Facilities)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")

    # Shaded post-takeover region
    x_min = df["month"].min()
    x_max = df["month"].max()
    ax.axvspan(takeover_ts, x_max, alpha=0.12, label="Post-takeover period")

    # Vertical marker
    ax.axvline(takeover_ts, linestyle="--", linewidth=1.6)
    ax.text(takeover_ts, ax.get_ylim()[1], " Took over (Jul 2023)", va="top")

    # Trendlines (simple linear regression pre vs post)
    # Using an integer time index for regression
    df["t"] = np.arange(len(df))

    pre = df[df["month"] < takeover_ts].copy()
    post = df[df["month"] >= takeover_ts].copy()

    def add_trendline(sub: pd.DataFrame, label: str):
        # Need at least 2 points to fit a line
        if len(sub) < 2:
            return
        m, b = np.polyfit(sub["t"].to_numpy(), sub["revenue"].to_numpy(), 1)
        y_hat = m * sub["t"].to_numpy() + b
        ax.plot(sub["month"], y_hat, linestyle="--", linewidth=2, label=label)

    add_trendline(pre, "Pre-takeover trend")
    add_trendline(post, "Post-takeover trend")

    ax.legend()

    _save(fig, out_dir / "monthly_revenue_total.png")


def plot_revenue_by_facility(
    monthly_by_facility: pd.DataFrame,
    out_dir: str | Path,
    takeover_date: str = "2023-07-01",
) -> None:
    out_dir = Path(out_dir)
    df = monthly_by_facility.copy()
    takeover_ts = pd.to_datetime(takeover_date)

    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(11, 5))

    sns.lineplot(
        data=df,
        x="month",
        y="revenue",
        hue="facility",
        marker="o",
        linewidth=2,
        ax=ax,
    )

    ax.set_title("Monthly Revenue by Facility")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")

    # Shaded post-takeover region
    x_max = df["month"].max()
    ax.axvspan(takeover_ts, x_max, alpha=0.12)

    # Vertical marker
    ax.axvline(takeover_ts, linestyle="--", linewidth=1.6)

    _save(fig, out_dir / "monthly_revenue_by_facility.png")