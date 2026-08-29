import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    report = {"starting_rows": len(df)}

    # Quantity ko number banao (agar text ki tarah save hai)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    # Date ko proper date format mein badlo
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Missing Category aur Region ko "Unknown" se bharo
    df["Category"] = df["Category"].fillna("Unknown")
    df["Region"] = df["Region"].fillna("Unknown")

    # Missing Revenue ko median (beech ki value) se bharo
    df["Revenue"] = df["Revenue"].fillna(df["Revenue"].median())

    # Duplicate rows hatao
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    df = df.reset_index(drop=True)
    report["final_rows"] = len(df)
    report["remaining_missing_values"] = int(df.isna().sum().sum())

    return df, report