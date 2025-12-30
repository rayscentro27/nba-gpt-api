import pandas as pd
from typing import Any

def df_preview(df: pd.DataFrame, limit: int = 10) -> list[dict[str, Any]]:
    if df is None or df.empty:
        return []
    return df.head(limit).where(pd.notnull(df), None).to_dict(orient="records")
