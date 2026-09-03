import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame, domain_config: dict) -> tuple[pd.DataFrame, dict]:
    report = {"starting_rows": len(df)}

    revenue_col = domain_config.get("revenue_column")
    category_col = domain_config.get("category_column")
    date_col = domain_config.get("date_column")
    quantity_col = domain_config.get("quantity_column")

    # Fix quantity column (if one was detected)
    if quantity_col and quantity_col in df.columns:
        df[quantity_col] = pd.to_numeric(df[quantity_col], errors="coerce")
        df[quantity_col] = df[quantity_col].fillna(df[quantity_col].median())

    # Fix date column (if one was detected)
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # Fix revenue column: strip currency symbols, convert to numeric
    if revenue_col and revenue_col in df.columns:
        df[revenue_col] = (
            df[revenue_col]
            .astype(str)
            .str.replace(r"[\$,₹]", "", regex=True)
            .replace({"nan": np.nan, "N/A": np.nan})
        )
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")
        df[revenue_col] = df[revenue_col].fillna(df[revenue_col].median())

    # Fill missing category with "Unknown"
    if category_col and category_col in df.columns:
        df[category_col] = df[category_col].fillna("Unknown")

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    # Handle any remaining missing values in OTHER columns too
    # (text columns -> "Unknown", numeric columns -> median)
    for col in df.columns:
        if df[col].isna().sum() == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")

    df = df.reset_index(drop=True)
    report["final_rows"] = len(df)
    report["remaining_missing_values"] = int(df.isna().sum().sum())

    return df, report