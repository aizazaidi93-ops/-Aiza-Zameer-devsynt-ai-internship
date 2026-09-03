from langgraph.graph import StateGraph, START, END
from agents.state import PipelineState
from agents.domain_agent import detect_domain
from agents.clean_agent import clean_data
from agents.analysis_agent import analyze_data
from agents.dashboard_agent import build_dashboard


def domain_node(state: PipelineState) -> PipelineState:
    filename_hint = state.get("dataset_filename", "")
    try:
        config = detect_domain(state["raw_data"], filename_hint)
        print("Domain Agent detected:", config)
    except Exception as e:
        print(f"Domain Agent failed ({e}). Falling back to safe defaults.")
        config = {
            "domain": "unknown",
            "revenue_column": None,
            "category_column": None,
            "date_column": None,
            "item_column": None,
            "quantity_column": None,
        }
    state["domain_config"] = config
    state["status"] = "domain_detected"
    return state


def clean_node(state: PipelineState) -> PipelineState:
    try:
        cleaned_df, report = clean_data(state["raw_data"], state["domain_config"])
        print("Clean Agent report:", report)
    except Exception as e:
        print(f"Clean Agent failed ({e}). Using raw data as-is.")
        cleaned_df = state["raw_data"]
        report = {"error": str(e)}
    state["cleaned_data"] = cleaned_df
    state["status"] = "cleaning_done"
    return state


def analysis_node(state: PipelineState) -> PipelineState:
    try:
        results = analyze_data(state["cleaned_data"], state["domain_config"])
    except Exception as e:
        print(f"Analysis Agent failed ({e}). Returning empty results.")
        results = {
            "domain": state["domain_config"].get("domain", "unknown"),
            "total_records": len(state["cleaned_data"]) if state["cleaned_data"] is not None else 0,
            "total_revenue": None,
            "average_value": None,
            "top_items": {},
            "by_category": {},
            "error": str(e),
        }
    state["analysis_results"] = results
    state["status"] = "analysis_done"
    return state


def dashboard_node(state: PipelineState) -> PipelineState:
    try:
        dashboard_info = build_dashboard(state["analysis_results"])
        print("Dashboard Agent generated:", dashboard_info)
    except Exception as e:
        print(f"Dashboard Agent failed ({e}). No dashboard generated.")
        dashboard_info = {"domain": state["analysis_results"].get("domain", "unknown"), "charts": [], "error": str(e)}
    state["dashboard_info"] = dashboard_info
    state["status"] = "dashboard_done"
    return state


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("domain", domain_node)
    graph.add_node("clean", clean_node)
    graph.add_node("analyze", analysis_node)
    graph.add_node("dashboard", dashboard_node)

    graph.add_edge(START, "domain")
    graph.add_edge("domain", "clean")
    graph.add_edge("clean", "analyze")
    graph.add_edge("analyze", "dashboard")
    graph.add_edge("dashboard", END)

    return graph.compile()