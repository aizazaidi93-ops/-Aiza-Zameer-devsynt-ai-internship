import pandas as pd
from agents.orchestrator import build_graph
from agents.visualization_agent import create_visualizations

# Raw dataset load karo
raw_df = pd.read_csv("data/retail_sales.csv")


graph = build_graph()

initial_state = {
    "raw_data": raw_df,
    "cleaned_data": None,
    "analysis_results": None,
    "status": "started",
}


final_state = graph.invoke(initial_state)

print("\n--- FINAL STATUS ---")
print(final_state["status"])

print("\n--- ANALYSIS RESULTS ---")
for key, value in final_state["analysis_results"].items():
    print(f"\n{key}:")
    print(value)


final_state["cleaned_data"].to_csv("data/retail_sales_cleaned.csv", index=False)
print("\nCleaned data saved to data/retail_sales_cleaned.csv")

create_visualizations(final_state["analysis_results"])