# src/cleaning.py
from __future__ import annotations

import pandas as pd


def standardize_columns(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(" ", "_")
          .str.replace("/", "_")
          .str.replace("(", "")
          .str.replace(")", "")
    )

    # Map to canonical names
    df = df.rename(columns={
        "visit_date": "encounter_date",
        "cpt___revenue": "cpt_code",
        "duration_min": "duration_min",
        "is_billable": "is_billable",
        "encounter_status": "encounter_status",
        "encounter_facility": "facility",
        "encounter_type": "encounter_type",
    })

    return df


def filter_individual_closed_billable(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["encounter_date"] = pd.to_datetime(out["encounter_date"], errors="coerce")
    out["duration_min"] = pd.to_numeric(out["duration_min"], errors="coerce").fillna(0)

    status = out["encounter_status"].astype(str).str.strip().str.lower()
    billable = out["is_billable"].astype(str).str.strip().str.lower()

    # Remove weird repeated header rows
    out = out[~status.eq("encounter status")]
    out = out[~billable.eq("is billable")]

    # Export uses Closed / Yes
    out = out[status.eq("closed") & billable.eq("yes")]

    # Exclude group encounters by text
    out["encounter_type"] = out["encounter_type"].astype(str)
    out = out[~out["encounter_type"].str.lower().str.contains("group", na=False)]

    # Drop missing
    out["cpt_code"] = out["cpt_code"].astype(str).str.strip()
    out = out.dropna(subset=["encounter_date", "cpt_code"])

    return out.reset_index(drop=True)