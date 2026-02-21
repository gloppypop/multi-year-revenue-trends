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


def plot_total_revenue(monthly_total: pd.DataFrame, out_dir: str | Path, takeover_date="2023-07-01") -> None:
    out_dir = Path(out_dir)
    df = monthly_total.copy()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x="month", y="revenue", marker="o", ax=ax)
    ax.set_title("Monthly Revenue (All Facilities)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")

    # Takeover marker
    ax.axvline(pd.to_datetime(takeover_date), linestyle="--", linewidth=1.5)
    ax.text(pd.to_datetime(takeover_date), ax.get_ylim()[1], " Took over (Jul 2023)", va="top")

    _save(fig, out_dir / "monthly_revenue_total.png")


def plot_revenue_by_facility(monthly_by_facility: pd.DataFrame, out_dir: str | Path, takeover_date="2023-07-01") -> None:
    out_dir = Path(out_dir)
    df = monthly_by_facility.copy()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x="month", y="revenue", hue="facility", marker="o", ax=ax)
    ax.set_title("Monthly Revenue by Facility")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")

    ax.axvline(pd.to_datetime(takeover_date), linestyle="--", linewidth=1.5)

    _save(fig, out_dir / "monthly_revenue_by_facility.png")