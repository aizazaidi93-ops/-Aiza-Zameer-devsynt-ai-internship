import pandas as pd


def analyze_data(df: pd.DataFrame, domain_config: dict) -> dict:
    results = {}
    results["domain"] = domain_config.get("domain", "unknown")

    revenue_col = domain_config.get("revenue_column")
    category_col = domain_config.get("category_column")
    item_col = domain_config.get("item_column")

    results["total_records"] = len(df)

    # Total revenue (if a revenue column was found)
    if revenue_col and revenue_col in df.columns:
        results["total_revenue"] = round(df[revenue_col].sum(), 2)
        results["average_value"] = round(df[revenue_col].mean(), 2)
    else:
        results["total_revenue"] = None
        results["average_value"] = None

    # Top items by revenue (if both item and revenue columns exist)
    if item_col and item_col in df.columns and revenue_col and revenue_col in df.columns:
        top_items = (
            df.groupby(item_col)[revenue_col]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        results["top_items"] = top_items.round(2).to_dict()
    else:
        results["top_items"] = {}

    # Revenue by category (if both category and revenue columns exist)
    if category_col and category_col in df.columns and revenue_col and revenue_col in df.columns:
        by_category = (
            df.groupby(category_col)[revenue_col]
            .sum()
            .sort_values(ascending=False)
        )
        results["by_category"] = by_category.round(2).to_dict()
    else:
        results["by_category"] = {}

    return results