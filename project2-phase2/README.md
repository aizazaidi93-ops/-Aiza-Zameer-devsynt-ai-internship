# Project2–Phase 2: Multi-Agent Retail Data Pipeline

**DevSynt AI Automation Internship** · Mentor: Afnan Shoukat · Individual Project

# Overview:

This project is a beginner-level multi-agent pipeline that takes a raw retail sales
dataset, cleans it, analyzes it, and presents the results on a static dashboard —
all coordinated by an orchestrator agent built with **LangGraph**.

The pipeline follows the **node → edge → state** pattern: an orchestrator decides
which agent runs next, and a shared "state" object carries the data (raw → cleaned
→ analyzed) between agents.

# Dataset Used:

A retail sales CSV ("data/retail_sales.csv") with the following columns:
"Order_ID, Date, Product, Category, Quantity, Region, Unit_Price, Revenue".

The raw dataset had 852 rows and included some real-world messiness: a few missing
values in "Category", "Region", and "Revenue", 2 duplicate rows, and a "Quantity"
column that wasn't stored as a proper number.

# Agents Built:

#1. Orchestrator Agent: ("agents/orchestrator.py")
The "manager" of the pipeline, built using LangGraph's `StateGraph`. It receives the
raw data and decides the processing order: **Clean Agent → Analysis Agent**. It
passes a shared `state` object (defined in `agents/state.py`) between the two nodes.

#2. Clean Agent: ("agents/clean_agent.py")
Takes the raw dataset and:
- Converts "Quantity" to a proper numeric type
- Converts "Date" to a proper date type
- Fills missing "Category" / "Region" values with `"Unknown"`
- Fills missing "Revenue" values with the median revenue
- Removes duplicate rows

See the before/after result in `assets/cleaning-result.png`.

#3. Analysis (EDA) Agent ("agents/analysis_agent.py")
Takes the cleaned data and generates key insights:
- Total sales and total orders
- Top 5 best-selling products
- Sales by region
- Sales by category
- Average order value

See the full output in "assets/analysis-output.png".

#4. Visualization Agent — Bonus ("agents/visualization_agent.py")
Takes the analysis results and generates 3 charts using "matplotlib", saved as PNG
files in the "assets/" folder:
- "top_products.png" — bar chart of the top 5 best-selling products
- "sales_by_region.png" — pie chart of sales by region
- "sales_by_category.png" — bar chart of sales by category

#Flow: Raw Data → Cleaned Data → Analysis → Dashboard

#5. Notes:
This was my first real multi-agent build. The biggest learning was understanding
how LangGraph's state object flows between nodes — once that clicked, connecting
the Clean and Analysis agents through the Orchestrator became straightforward.