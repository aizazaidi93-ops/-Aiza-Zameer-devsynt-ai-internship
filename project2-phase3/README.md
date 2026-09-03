# Project 2 – Phase 3: Domain-Aware Multi-Agent Data Pipeline

**DevSynt AI Automation Internship** · Mentor: Afnan Shoukat · Final Build Phase

## Overview

This is the production-grade evolution of the Phase 2 retail pipeline. Where Phase 2
worked reliably on a single, fixed dataset, this version is **domain-aware**: it
inspects any incoming dataset, figures out what kind of business data it's looking
at, and configures the rest of the pipeline — cleaning rules, analysis logic, and
the dashboard itself — to match. It was built once and tested successfully across
**5 structurally different datasets** spanning 5 different domains.

The goal wasn't to build something that only works on the dataset it was tested on.
It was to build something that generalizes — the difference between a demo and a
product.

## What Changed From Phase 2

| | Phase 2 | Phase 3 |
|---|---|---|
| Works on | One fixed retail dataset | Any dataset, any domain |
| Column mapping | Hardcoded column names | Auto-detected by the Domain Configuration Agent |
| Dashboard | Static, fixed chart types | Dynamically generated based on what data is available |
| Failure behavior | Would break on unexpected structure | Fails gracefully, falls back to safe defaults |
| Prompts | Fixed | Iterated based on real testing failures (see Prompt Evolution Log) |

## Architecture
Raw Dataset
│
▼
Domain Configuration Agent   ← NEW. Inspects columns + sample rows, identifies
│                          the domain (retail, restaurant, inventory, etc.)
│                          and maps which column is revenue, category,
│                          date, item, and quantity.
▼
Orchestrator Agent           ← Coordinates the rest of the pipeline using
│                          LangGraph's StateGraph, passing the domain
│                          config downstream to every agent.
▼
Clean Agent                  ← Uses the domain config instead of hardcoded
│                          column names to fix types, remove duplicates,
│                          and fill missing values across every column.
▼
Analysis Agent                ← Computes total records, total value, average
│                          value, top items, and category breakdown —
│                          using whichever columns the domain config points to.
▼
Dashboard Agent               ← NEW. Only builds the charts that the available
│                          data actually supports, then generates a
│                          matching HTML dashboard from scratch — title,
│                          cards, and chart layout all adapt to the domain.
▼
Dynamic Dashboard (output)
See `assets/flow-diagram.png` for the visual version.

## Domain Configuration Agent — How It Works

This is the core addition in Phase 3. Before any cleaning or analysis happens, this
agent:
1. Reads the dataset's column names and a few sample rows.
2. Sends them to Gemini with a prompt asking it to classify the domain and map
   five roles: revenue column, category column, date column, item column, and
   quantity column.
3. Returns a small config object (e.g. `{"domain": "restaurant", "revenue_column":
   "bill_amount", "item_column": "dish_name", ...}`) that every downstream agent
   reads instead of assuming fixed column names.

This is what lets the same code run against a retail sales sheet, a restaurant
POS export, an inventory log, and a SaaS subscription report without being
rewritten for each one.

## Tested Across 5 Domains

| # | Dataset | Detected Domain | Revenue Column | Item Column | Result |
|---|---|---|---|---|---|
| 1 | `retail_sales.csv` | Retail | Revenue | Product | ✅ Clean run |
| 2 | `restaurant_sales.csv` | Restaurant | bill_amount | dish_name | ✅ Clean run |
| 3 | `inventory_stock.csv` | Inventory | unit_cost | item_name | ✅ Clean run |
| 4 | `ecommerce_orders.csv` | Ecommerce | order_total | product_title | ✅ Clean run |
| 5 | `subscription_metrics.csv` | Subscription | monthly_revenue | plan_type | ✅ Clean run |

Every dataset had intentional real-world messiness built in: missing values,
duplicate rows, inconsistent data types, and currency-formatted strings — the
Clean Agent handled all of it using the domain config, with **zero remaining
missing values** in the final output across every dataset.

Screenshots of each dataset's generated dashboard are in `assets/dataset1-result.png`
through `assets/dataset5-result.png`.

## Prompt Evolution

The Domain Configuration Agent's prompt wasn't right on the first attempt. Testing
against the subscription dataset revealed it was picking a unique identifier
(`subscription_id`) as the "item" column, which made the top-items analysis
meaningless. It also became clear the Clean Agent was only fixing the columns
the Domain Agent explicitly flagged, leaving missing values in every other column.

Both issues were fixed by:
- Adding an explicit rule to the prompt: the item column must be a *repeatable*
  entity (a product, dish, or plan name), never a unique ID.
- Adding a catch-all cleanup pass in the Clean Agent that handles missing values
  in every remaining column, not just the ones the Domain Agent flagged.

Full details, including before/after results, are documented in
`assets/prompt-evolution-log.md`.

## Error Handling

Every stage of the pipeline (`domain`, `clean`, `analyze`, `dashboard`) is wrapped
in a try/except block. If any stage fails — a bad API response, a completely
unrecognizable dataset, missing columns — the pipeline logs what went wrong and
falls back to safe defaults instead of crashing. This was verified by running the
pipeline against a deliberately broken, near-empty CSV: the pipeline completed
end-to-end, correctly reported the domain as "other," and produced an empty but
valid dashboard rather than throwing an unhandled exception.

## Key Results (Retail Dataset Example)

| Metric | Value |
|---|---|
| Total Records | 850 |
| Total Value | ₹956,508.86 |
| Average Value | ₹1,125.30 |
| Top Item | Laptop |
| Detected Domain | Retail |

## How to Run

1. Activate the virtual environment: `venv\Scripts\activate`
2. Install dependencies: `pip install langchain langgraph langchain-google-genai pandas matplotlib python-dotenv`
3. Add your Gemini API key to a `.env` file: `GEMINI_API_KEY=your_key_here`
4. Set which dataset to test in `main.py`:
   ```python
   DATASET_PATH = "test-datasets/retail_sales.csv"

Folder Structure
project2-phase3/
  agents/
    orchestrator.py       Coordinates the pipeline (LangGraph StateGraph)
    domain_agent.py        Detects domain + maps key columns (NEW)
    clean_agent.py          Domain-aware data cleaning
    analysis_agent.py       Domain-aware insight generation
    dashboard_agent.py      Builds charts + HTML dynamically (NEW)
    state.py                 Shared pipeline state definition
  test-datasets/
    retail_sales.csv
    restaurant_sales.csv
    inventory_stock.csv
    ecommerce_orders.csv
    subscription_metrics.csv
  assets/
    flow-diagram.png
    dataset1-result.png … dataset5-result.png
    prompt-evolution-log.md
  dashboard/
    index.html              Auto-generated by the Dashboard Agent
  data/
    cleaned_output.csv       Cleaned output from the most recent run
  main.py
  README.md

Notes
The hardest part of this phase wasn't writing the agents — it was accepting that
the first version of the Domain Agent's prompt would be wrong in ways I couldn't
predict until I actually ran it against different data. Testing across 5 real
(if synthetic) domains surfaced two concrete failures that a single-dataset test
never would have caught. That iterative loop — test, observe the failure, tighten
the prompt or logic, retest — is what actually made this feel like a "production"
system rather than a script that happens to work once.