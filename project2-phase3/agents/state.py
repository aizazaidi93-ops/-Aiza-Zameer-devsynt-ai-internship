from typing_extensions import TypedDict
import pandas as pd

class PipelineState(TypedDict):
    raw_data: pd.DataFrame
    cleaned_data: pd.DataFrame
    analysis_results: dict
    domain_config: dict
    dashboard_info: dict
    dataset_filename: str
    status: str