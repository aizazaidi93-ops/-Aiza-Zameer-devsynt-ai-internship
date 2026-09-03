import matplotlib.pyplot as plt

# Consistent professional color palette (same as Phase 2)
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


def build_dashboard(analysis_results: dict, output_folder: str = "assets",
                     dashboard_folder: str = "dashboard") -> dict:
    """
    Dynamically builds whichever charts make sense for the data that's
    actually available in analysis_results, then generates a matching
    HTML dashboard page — all driven by what data is actually present,
    not hardcoded to one domain's shape.
    """
    generated = {
        "domain": analysis_results.get("domain", "unknown"),
        "charts": [],
    }

    top_items = analysis_results.get("top_items") or {}
    by_category = analysis_results.get("by_category") or {}

    # Chart 1: Top items (only if we actually have item-level data)
    if top_items:
        items = list(top_items.keys())
        values = list(top_items.values())

        fig, ax = plt.subplots(figsize=(6, 4.6), dpi=150)
        ax.bar(items, values, color=PALETTE[:len(items)], width=0.6,
               edgecolor="white", linewidth=0.5, zorder=3)
        ax.set_title("Top Items by Value", fontsize=13, fontweight="bold", color=NAVY, pad=14)
        ax.set_ylabel("Value", fontsize=10, color="#475569")
        style_ax(ax)
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(f"{output_folder}/chart_top_items.png", dpi=150)
        plt.close()
        generated["charts"].append({"file": "chart_top_items.png", "title": "Top Items by Value"})

# Chart 2: By category (donut chart, only if category data exists)
    if by_category:
        total = sum(by_category.values())
        sorted_items = sorted(by_category.items(), key=lambda x: x[1], reverse=True)

        # Combine any slice smaller than 3% of the total into "Other"
        # (prevents invisible/overlapping slivers on the chart)
        main_items = []
        other_total = 0
        for name, value in sorted_items:
            if total > 0 and (value / total) < 0.03:
                other_total += value
            else:
                main_items.append((name, value))

        if other_total > 0:
            main_items.append(("Other", other_total))

        categories = [k for k, v in main_items]
        cat_values = [v for k, v in main_items]

        fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=150)
        wedges, texts, autotexts = ax.pie(
            cat_values,
            colors=PALETTE[:len(categories)],
            autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
            startangle=90,
            pctdistance=0.75,
            wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
            textprops={"fontsize": 10, "color": "white", "fontweight": "bold"},
        )
        ax.legend(
            wedges, categories,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=10,
            frameon=False,
        )
        ax.set_title("Breakdown by Category", fontsize=13, fontweight="bold", color=NAVY, pad=14)
        plt.tight_layout()
        plt.savefig(f"{output_folder}/chart_by_category.png", dpi=150, bbox_inches="tight")
        plt.close()
        generated["charts"].append({"file": "chart_by_category.png", "title": "Breakdown by Category"})
    

    # ---- Build the HTML dashboard dynamically ----
    domain_label = generated["domain"].replace("_", " ").title()
    total_records = analysis_results.get("total_records", "N/A")
    total_revenue = analysis_results.get("total_revenue")
    average_value = analysis_results.get("average_value")

    total_revenue_display = f"₹{total_revenue:,.2f}" if total_revenue is not None else "N/A"
    average_value_display = f"₹{average_value:,.2f}" if average_value is not None else "N/A"

    # Build chart cards HTML for whichever charts actually got generated
    chart_cards_html = ""
    for chart in generated["charts"]:
        chart_cards_html += f"""
    <div class="chart-card">
        <h3>{chart['title']}</h3>
        <img src="../assets/{chart['file']}" alt="{chart['title']}">
    </div>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{domain_label} Dashboard</title>
<style>
    * {{ box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', Arial, sans-serif;
        background: linear-gradient(160deg, #f8fafc 0%, #e8ecf3 100%);
        margin: 0;
        padding: 40px 30px;
        min-height: 100vh;
    }}
    .header {{ text-align: center; margin-bottom: 40px; }}
    .header h1 {{ color: #141c2d; font-size: 34px; margin: 0; letter-spacing: -0.5px; }}
    .header p {{ color: #64748b; font-size: 15px; margin-top: 8px; }}
    .cards {{
        display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;
        margin-bottom: 45px; max-width: 1200px; margin-left: auto; margin-right: auto;
    }}
    .card {{
        background: #ffffff; border-radius: 16px; padding: 26px 34px;
        box-shadow: 0 4px 18px rgba(20, 28, 45, 0.08); text-align: center;
        min-width: 210px; flex: 1; border-top: 4px solid var(--accent, #2563eb);
    }}
    .card .icon {{ font-size: 22px; margin-bottom: 6px; }}
    .card h2 {{ margin: 4px 0 0; color: #141c2d; font-size: 26px; font-weight: 700; }}
    .card p {{
        margin: 6px 0 0; color: #6b7686; font-size: 13px;
        text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;
    }}
    .card.c1 {{ --accent: #1e3a8a; }}
    .card.c2 {{ --accent: #2563eb; }}
    .card.c3 {{ --accent: #0d9488; }}
    .charts {{
        display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;
        max-width: 1300px; margin: 0 auto;
    }}
    .chart-card {{
        background: #ffffff; border-radius: 16px; padding: 20px;
        box-shadow: 0 4px 18px rgba(20, 28, 45, 0.08); flex: 1;
        min-width: 340px; max-width: 420px;
    }}
    .chart-card h3 {{ color: #141c2d; font-size: 15px; margin: 0 0 12px 4px; font-weight: 600; }}
    .chart-card img {{ width: 100%; border-radius: 10px; display: block; }}
    .footer {{ text-align: center; margin-top: 45px; color: #94a3b8; font-size: 13px; }}
</style>
</head>
<body>

<div class="header">
    <h1>📊 {domain_label} Dashboard</h1>
    <p>Auto-generated by the Dashboard Agent based on detected domain: {domain_label}</p>
</div>

<div class="cards">
    <div class="card c1">
        <div class="icon">📦</div>
        <h2>{total_records}</h2>
        <p>Total Records</p>
    </div>
    <div class="card c2">
        <div class="icon">💰</div>
        <h2>{total_revenue_display}</h2>
        <p>Total Value</p>
    </div>
    <div class="card c3">
        <div class="icon">📈</div>
        <h2>{average_value_display}</h2>
        <p>Average Value</p>
    </div>
</div>

<div class="charts">{chart_cards_html}
</div>

<div class="footer">
    Built with LangGraph &middot; Domain-Aware Multi-Agent Pipeline
</div>

</body>
</html>
"""

    with open(f"{dashboard_folder}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    generated["html_file"] = f"{dashboard_folder}/index.html"
    return generated