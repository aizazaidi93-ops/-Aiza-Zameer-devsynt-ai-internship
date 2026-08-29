import pandas as pd

def analyze_data(df: pd.DataFrame) -> dict:
    results = {}

    # Total sales (Revenue column ka total)
    results["total_sales"] = round(df["Revenue"].sum(), 2)

    # Total orders
    results["total_orders"] = len(df)

    # Best-selling products (Revenue ke hisaab se top 5)
    top_products = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    results["top_products"] = top_products.round(2).to_dict()

    # Region-wise sales
    sales_by_region = (
        df.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    results["sales_by_region"] = sales_by_region.round(2).to_dict()

    # Category-wise sales
    sales_by_category = (
        df.groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    results["sales_by_category"] = sales_by_category.round(2).to_dict()

    # Average order value
    results["average_order_value"] = round(df["Revenue"].mean(), 2)

    return results