from langgraph.graph import StateGraph, START, END
from agents.state import PipelineState
from agents.clean_agent import clean_data
from agents.analysis_agent import analyze_data


def clean_node(state: PipelineState) -> PipelineState:
    cleaned_df, report = clean_data(state["raw_data"])
    print("Clean Agent report:", report)
    state["cleaned_data"] = cleaned_df
    state["status"] = "cleaning_done"
    return state


def analysis_node(state: PipelineState) -> PipelineState:
    results = analyze_data(state["cleaned_data"])
    state["analysis_results"] = results
    state["status"] = "analysis_done"
    return state


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("clean", clean_node)
    graph.add_node("analyze", analysis_node)

    graph.add_edge(START, "clean")
    graph.add_edge("clean", "analyze")
    graph.add_edge("analyze", END)

    return graph.compile()