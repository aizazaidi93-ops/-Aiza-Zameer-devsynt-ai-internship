import os
import json
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)


def detect_domain(df: pd.DataFrame, filename_hint: str = "") -> dict:
    columns = list(df.columns)
    sample_rows = df.head(3).to_dict(orient="records")

    hint_line = f'The source filename is "{filename_hint}" — use it as a hint if it clarifies the domain.\n' if filename_hint else ""

    prompt = f"""
You are a data analyst. Look at this dataset's columns and sample rows,
and identify the domain and key columns.

{hint_line}Columns: {columns}
Sample rows: {json.dumps(sample_rows, default=str)}

Important rules:
- "item_column" must be a REPEATABLE entity name (like a product, dish,
  service, or plan name) that would naturally repeat across multiple rows.
  Do NOT choose a column that looks like a unique identifier (e.g. an
  order ID, subscription ID, SKU, or transaction number) — if no repeatable
  entity column exists, set item_column to null.
- "revenue_column" should be a monetary amount per record (price, cost,
  revenue, bill, total, fee) — not a quantity or an identifier.

Respond ONLY with valid JSON in this exact format, no extra text:
{{
  "domain": "short label like retail, restaurant, inventory, ecommerce, subscription, or other",
  "revenue_column": "exact column name that represents money/amount/revenue, or null if none",
  "category_column": "exact column name that represents a category/group/type, or null if none",
  "date_column": "exact column name that represents a date, or null if none",
  "item_column": "exact column name that represents the main product/item/entity name, or null if none",
  "quantity_column": "exact column name that represents quantity/count, or null if none"
}}
"""

    response = llm.invoke(prompt)

    content = response.content
    if isinstance(content, list):
        text = "".join(
            part if isinstance(part, str) else part.get("text", "")
            for part in content
        ).strip()
    else:
        text = content.strip()

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()

    try:
        config = json.loads(text)
    except json.JSONDecodeError:
        config = {
            "domain": "unknown",
            "revenue_column": None,
            "category_column": None,
            "date_column": None,
            "item_column": None,
            "quantity_column": None,
        }

    return config