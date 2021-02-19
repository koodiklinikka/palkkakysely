from typing import Optional

import pandas as pd


def get_categorical_stats(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
    *,
    na_as_category: Optional[str] = None,
) -> pd.DataFrame:
    # Drop records where value is not numeric before grouping...
    df = df.copy()
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df[df[value_col].notna() & df[value_col] > 0]
    if na_as_category:
        df[category_col] = df[category_col].astype("string")
        df.loc[df[category_col].isna(), category_col] = na_as_category
        df[category_col] = df[category_col].astype("category")
    # ... then carry on.
    group = df[[category_col, value_col]].groupby(category_col)
    return group[value_col].agg(["mean", "min", "max", "median", "count"])
