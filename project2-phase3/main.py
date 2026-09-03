import pandas as pd
from agents.orchestrator import build_graph

# Which dataset to test on — change this line to test different domains
DATASET_PATH = "test-datasets/subscription_metrics.csv"

# Raw dataset load karo
raw_df = pd.read_csv(DATASET_PATH)
filename = DATASET_PATH.split("/")[-1]

# Graph banao
graph = build_graph()

# Initial state
initial_state = {
    "raw_data": raw_df,
    "cleaned_data": None,
    "analysis_results": None,
    "domain_config": None,
    "dashboard_info": None,
    "dataset_filename": filename,
    "status": "started",
}

# Pipeline chalao
final_state = graph.invoke(initial_state)

print("\n--- FINAL STATUS ---")
print(final_state["status"])

print("\n--- DOMAIN CONFIG ---")
print(final_state["domain_config"])

print("\n--- ANALYSIS RESULTS ---")
for key, value in final_state["analysis_results"].items():
    print(f"\n{key}:")
    print(value)

print("\n--- DASHBOARD INFO ---")
print(final_state["dashboard_info"])

# Cleaned data ko save karo
final_state["cleaned_data"].to_csv("data/cleaned_output.csv", index=False)
print("\nCleaned data saved to data/cleaned_output.csv")