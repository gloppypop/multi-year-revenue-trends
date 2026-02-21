# src/rate_table.py
from __future__ import annotations

import pandas as pd

# FY definitions:
# FY23: Oct 2022 - Sep 2023
# FY24: Oct 2023 - Sep 2024
# FY25: Oct 2024 - Sep 2025
# FY26: Oct 2025 - Sep 2026

RATES_FY23 = {
    "90832": 65.00,
    "90834": 100.00,
    "90837": 129.00,
    "H0001": 176.00,
    "H0006": 45.50,
    "T1012": 47.50,   # per encounter
    "T1007": 117.00,  # per encounter (per unit regardless of time)
    "H0004": 26.50,   # 15-min units
    "H0038": 24.00,   # 15-min units
}

RATES_FY24 = {
    "90832": 71.50,
    "90834": 110.00,
    "90837": 142.00,
    "H0001": 194.00,
    "H0006": 50.50,
    "T1012": 52.50,
    "T1007": 129.00,
    "H0004": 29.50,
    "H0038": 26.50,
}

RATES_FY25 = dict(RATES_FY24)
RATES_FY26 = dict(RATES_FY25)

RATE_TABLES = {
    "FY23": RATES_FY23,
    "FY24": RATES_FY24,
    "FY25": RATES_FY25,
    "FY26": RATES_FY26,
}

TIME_BASED_CODES = {"H0004", "H0038"}   # 15-min units
PER_ENCOUNTER_CODES = {"90832", "90834", "90837", "H0001", "H0006", "T1012", "T1007"}


def fiscal_year(dt: pd.Timestamp) -> str:
    """Return FYxx based on an Oct-Sep fiscal year."""
    if pd.isna(dt):
        return "UNKNOWN"
    fy = dt.year + 1 if dt.month >= 10 else dt.year
    return f"FY{str(fy)[-2:]}"


def get_rate(cpt_code: str, fy: str) -> float:
    """Look up a CPT rate for a given fiscal year."""
    return float(RATE_TABLES.get(fy, {}).get(str(cpt_code), 0.0))