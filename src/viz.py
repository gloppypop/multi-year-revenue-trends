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
    takeover_date: str = "2023-08-01",
) -> None:
    import numpy as np

    out_dir = Path(out_dir)
    df = monthly_total.copy()
    takeover_ts = pd.to_datetime(takeover_date)

    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(11, 5))

    # Main revenue line
    sns.lineplot(
        data=df,
        x="month",
        y="revenue",
        marker="o",
        linewidth=2,
        ax=ax,
    )

    ax.set_title("Monthly Revenue (All Facilities)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")

    # Shade post-takeover region
    x_max = df["month"].max()
    ax.axvspan(takeover_ts, x_max, alpha=0.12, label="Post-takeover period")

    # Vertical marker
    ax.axvline(takeover_ts, linestyle="--", linewidth=1.6)
    ax.text(takeover_ts, ax.get_ylim()[1], " Took over (Aug 2023)", va="top")

    # Split into pre/post for summary stats
    pre = df[df["month"] < takeover_ts].copy()
    post = df[df["month"] >= takeover_ts].copy()

    # Add pre vs post averages on the chart
    if len(pre) >= 1 and len(post) >= 1:
        pre_avg = float(pre["revenue"].mean())
        post_avg = float(post["revenue"].mean())

        if pre_avg > 0:
            pct = (post_avg / pre_avg - 1) * 100
        else:
            pct = np.nan

        # Put "stats box" in the top-left
        stats_text = (
            f"Avg monthly revenue (pre):  ${pre_avg:,.0f}\n"
            f"Avg monthly revenue (post): ${post_avg:,.0f}\n"
            f"Change: {pct:+.1f}%"
        )

        ax.text(
            0.02,
            0.92,
            stats_text,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.80),
        )

    # Post-takeover trendline
    df["t"] = np.arange(len(df))
    post = df[df["month"] >= takeover_ts].copy()

    if len(post) >= 2:
        m, b = np.polyfit(post["t"].to_numpy(), post["revenue"].to_numpy(), 1)
        y_hat = m * post["t"].to_numpy() + b
        ax.plot(
            post["month"],
            y_hat,
            linestyle="--",
            linewidth=2.2,
            label="Post-takeover trend",
        )

    ax.legend()

    _save(fig, out_dir / "monthly_revenue_total.png")


def plot_revenue_by_facility(
    monthly_by_facility: pd.DataFrame,
    out_dir: str | Path,
    takeover_date: str = "2023-08-01",
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