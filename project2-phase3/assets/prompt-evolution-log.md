# Prompt Evolution Log

This log documents how the Domain Configuration Agent's prompt was refined
based on real failures observed while testing across 5 different-domain
datasets: retail, restaurant, inventory, e-commerce, and subscription.

---

## Testing Round 1 — Initial Prompt

**Prompt behavior:** Asked Gemini to identify domain and key columns
(revenue, category, date, item, quantity) with no additional constraints
beyond the JSON output format.

**Datasets tested:** retail_sales.csv, restaurant_sales.csv,
inventory_stock.csv, ecommerce_orders.csv, subscription_metrics.csv

**Results:**
- Retail, restaurant, inventory, and e-commerce datasets: columns detected
  correctly on the first try.
- Subscription dataset: `item_column` was incorrectly set to
  `subscription_id` — a unique identifier, not a repeatable entity. This
  made the "top items" analysis meaningless (it just listed random
  subscription IDs instead of showing which plan type generated the most
  revenue).
- All datasets: a noticeable number of missing values remained after
  cleaning (`remaining_missing_values` was non-zero across every dataset).
  This was because the Clean Agent only filled missing values in the
  columns the Domain Agent explicitly flagged (revenue, category), leaving
  other columns (e.g. `waiter`, `warehouse`, `payment_method`) untouched.

**Issues identified:**
1. The Domain Agent had no rule preventing it from picking a unique-ID-like
   column as the "item" column.
2. The Clean Agent's missing-value handling was too narrow — it only
   covered the columns flagged by the Domain Agent.

---

## Testing Round 2 — Refined Prompt

**Changes made:**

1. **Domain Agent prompt** — added explicit rules:
   - `item_column` must be a *repeatable* entity name (product, dish, plan,
     service) that would naturally appear more than once in the dataset.
   - Explicitly instructed the model to avoid choosing unique identifiers
     (order IDs, subscription IDs, SKUs, transaction numbers) as the item
     column, and to return `null` if no such repeatable column exists.
   - Clarified that `revenue_column` should represent a monetary amount
     per record, not a quantity or an identifier.

2. **Clean Agent** — added a general-purpose cleanup pass at the end of
   `clean_data()`: after handling the domain-specific columns, it now
   loops through every remaining column and fills missing values
   (numeric columns → median, text columns → "Unknown") instead of only
   touching the columns the Domain Agent flagged.

**Results after refinement:**
- Subscription dataset: `item_column` correctly changed to `plan_type`,
  and `top_items` now shows meaningful results (Enterprise, Business, Pro,
  Basic) instead of random subscription IDs.
- All 5 datasets: `remaining_missing_values` dropped to `0` across the
  board.

---

## Summary

| Round | Issue | Fix | Outcome |
|---|---|---|---|
| 1 | `item_column` picked a unique ID (subscription dataset) | Added explicit "repeatable entity, not a unique ID" rule to the prompt | Correctly picks `plan_type` instead |
| 1 | Missing values remained in non-flagged columns across all datasets | Added a catch-all cleanup loop in Clean Agent for every column | `remaining_missing_values` = 0 on all 5 datasets |

This iterative process — test on real, varied data, observe where the
agent's output breaks down, then tighten the prompt or logic — is what
turned the Phase 2 prototype into a pipeline that reliably generalizes
across domains rather than only working on the dataset it was built for.