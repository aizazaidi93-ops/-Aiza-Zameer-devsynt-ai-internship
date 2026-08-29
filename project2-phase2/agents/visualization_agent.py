import matplotlib.pyplot as plt

def create_visualizations(analysis_results: dict, output_folder: str = "assets"):
    # Chart 1: Top Products (Bar Chart)
    products = list(analysis_results["top_products"].keys())
    values = list(analysis_results["top_products"].values())

    plt.figure(figsize=(8, 5))
    plt.bar(products, values, color="#3b82f6")
    plt.title("Top 5 Best-Selling Products")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/top_products.png")
    plt.close()

    # Chart 2: Sales by Region (Pie Chart)
    regions = list(analysis_results["sales_by_region"].keys())
    region_values = list(analysis_results["sales_by_region"].values())

    plt.figure(figsize=(6, 6))
    plt.pie(region_values, labels=regions, autopct="%1.1f%%")
    plt.title("Sales by Region")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sales_by_region.png")
    plt.close()

    # Chart 3: Sales by Category (Bar Chart)
    categories = list(analysis_results["sales_by_category"].keys())
    category_values = list(analysis_results["sales_by_category"].values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, category_values, color="#10b981")
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sales_by_category.png")
    plt.close()

    print("Charts saved in the 'assets' folder!")