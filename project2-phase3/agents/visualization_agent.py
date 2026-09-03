import matplotlib.pyplot as plt

# Consistent professional color palette used across all charts
PALETTE = ["#1e3a8a", "#2563eb", "#0d9488", "#d97706", "#7c3aed"]
NAVY = "#1e293b"
LIGHT_GRID = "#e2e8f0"


def style_ax(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")
    ax.tick_params(colors="#475569", labelsize=10)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=LIGHT_GRID, linewidth=1)


def create_visualizations(analysis_results: dict, output_folder: str = "assets"):
    # Chart 1: Top Products (Bar Chart)
    products = list(analysis_results["top_products"].keys())
    values = list(analysis_results["top_products"].values())

    fig, ax = plt.subplots(figsize=(6, 4.6), dpi=150)
    ax.bar(products, values, color=PALETTE[:len(products)], width=0.6,
           edgecolor="white", linewidth=0.5, zorder=3)
    ax.set_title("Top 5 Best-Selling Products", fontsize=13, fontweight="bold", color=NAVY, pad=14)
    ax.set_ylabel("Revenue", fontsize=10, color="#475569")
    style_ax(ax)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/top_products.png", dpi=150)
    plt.close()

    # Chart 2: Sales by Region (Donut Chart)
    regions = list(analysis_results["sales_by_region"].keys())
    region_values = list(analysis_results["sales_by_region"].values())

    fig, ax = plt.subplots(figsize=(5.6, 5.2), dpi=150)
    wedges, texts, autotexts = ax.pie(
        region_values,
        labels=regions,
        colors=PALETTE[:len(regions)],
        autopct=lambda p: f"{p:.1f}%" if p > 1 else "",
        startangle=90,
        pctdistance=0.75,
        labeldistance=1.08,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
        textprops={"fontsize": 10.5, "color": NAVY},
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(9.5)
        at.set_fontweight("bold")
    ax.set_title("Sales by Region", fontsize=13, fontweight="bold", color=NAVY, pad=14)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sales_by_region.png", dpi=150)
    plt.close()

    # Chart 3: Sales by Category (Bar Chart)
    categories = list(analysis_results["sales_by_category"].keys())
    category_values = list(analysis_results["sales_by_category"].values())

    fig, ax = plt.subplots(figsize=(6, 4.6), dpi=150)
    ax.bar(categories, category_values, color=PALETTE[:len(categories)], width=0.6,
           edgecolor="white", linewidth=0.5, zorder=3)
    ax.set_title("Sales by Category", fontsize=13, fontweight="bold", color=NAVY, pad=14)
    ax.set_ylabel("Revenue", fontsize=10, color="#475569")
    style_ax(ax)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sales_by_category.png", dpi=150)
    plt.close()

    print("Charts saved in the 'assets' folder!")