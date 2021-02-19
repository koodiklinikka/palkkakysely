from bokeh import models as bm, plotting as bp
from bokeh.transform import factor_cmap
from pandas import DataFrame

from data_utils import get_categorical_stats

CAT_Q_RADIUS = 0.1

gender_colormap = factor_cmap("Sukupuoli", ["#4834d4", "#eb4d4b"], ["mies", "nainen"])


def get_df_hover_tool(df: DataFrame):
    return bm.HoverTool(tooltips=[(c, f"@{{{c}}}") for c in df.columns])


def set_yaxis_cash(plot):
    plot.yaxis.axis_label = "Vuositulot"
    plot.yaxis[0].formatter = bm.NumeralTickFormatter(format="€0")


def get_categorical_stats_plot(df, *, category, value, na_as_category=None):
    df = get_categorical_stats(df, category, value, na_as_category=na_as_category)
    df.reset_index(inplace=True)
    df[category] = df[category].astype("category")
    plot = bp.figure(
        title=f"{category}/{value}", x_range=list(df[category].cat.categories)
    )
    set_yaxis_cash(plot)
    plot.vbar(
        df[category],
        CAT_Q_RADIUS * 2.5,
        df["max"],
        df["min"],
        color="#a4b0be",
        fill_alpha=0.7,
    )
    plot.circle(
        df[category],
        df["q25"],
        radius=CAT_Q_RADIUS,
        legend_label="q25",
        color="#f368e0",
    )
    plot.circle(
        df[category],
        df["q75"],
        radius=CAT_Q_RADIUS,
        legend_label="q75",
        color="#00d2d3",
    )
    plot.circle(
        df[category],
        df["q90"],
        radius=CAT_Q_RADIUS,
        legend_label="q90",
        color="#ff9f43",
    )
    plot.line(
        df[category], df["median"], legend_label="median", color="#1289A7", line_width=4
    )
    plot.line(
        df[category], df["mean"], legend_label="mean", color="#B53471", line_width=4
    )
    return plot
