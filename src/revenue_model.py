# src/revenue_model.py
from __future__ import annotations

import numpy as np
import pandas as pd

from src.rate_table import TIME_BASED_CODES, fiscal_year, get_rate


def add_units_and_revenue(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["fy"] = out["encounter_date"].apply(fiscal_year)
    out["month"] = out["encounter_date"].dt.to_period("M").dt.to_timestamp()

    # Default: per encounter / per unit = 1
    out["units"] = 1

    # Time-based: 15-minute units
    is_time = out["cpt_code"].isin(TIME_BASED_CODES)
    out.loc[is_time, "units"] = np.floor(out.loc[is_time, "duration_min"] / 15).astype(int).clip(lower=0)

    # Rate lookup by CPT + FY
    out["rate"] = out.apply(lambda r: get_rate(r["cpt_code"], r["fy"]), axis=1)
    out["revenue"] = out["units"] * out["rate"]

    return out


def rollups(encounter_level: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = encounter_level.copy()

    monthly_total = (
        df.groupby("month", as_index=False)
          .agg(
              encounters=("cpt_code", "size"),
              client_hours=("duration_min", lambda x: x.sum() / 60.0),
              total_units=("units", "sum"),
              revenue=("revenue", "sum"),
          )
          .sort_values("month")
    )

    monthly_by_facility = (
        df.groupby(["month", "facility"], as_index=False)
          .agg(
              encounters=("cpt_code", "size"),
              total_units=("units", "sum"),
              revenue=("revenue", "sum"),
          )
          .sort_values(["month", "facility"])
    )

    monthly_by_code = (
        df.groupby(["month", "cpt_code"], as_index=False)
          .agg(
              encounters=("cpt_code", "size"),
              total_units=("units", "sum"),
              revenue=("revenue", "sum"),
          )
          .sort_values(["month", "cpt_code"])
    )

    return monthly_total, monthly_by_facility, monthly_by_code