import pandas as pd


def get_categorical_stats(
    df: pd.DataFrame, category_col: str, value_col: str
) -> pd.DataFrame:
    # Drop records where value is not numeric before grouping...
    df = df.copy()
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df[df[value_col].notna() & df[value_col] > 0]
    # ... then carry on.
    group = df[[category_col, value_col]].groupby(category_col)
    return group[value_col].agg(["mean", "min", "max", "median"])
