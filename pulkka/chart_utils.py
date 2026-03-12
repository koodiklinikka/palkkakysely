from bokeh import models as bm
from bokeh import plotting as bp
from bokeh.transform import factor_cmap
from pandas import DataFrame, Series

from pulkka.data_utils import explode_multiselect, get_categorical_stats

CAT_Q_RADIUS = 0.1

gender_colormap = factor_cmap("Sukupuoli", ["#4834d4", "#eb4d4b"], ["mies", "nainen"])


def get_df_hover_tool(df: DataFrame):
    return bm.HoverTool(tooltips=[(c, f"@{{{c}}}") for c in df.columns])


def set_yaxis_cash(plot):
    plot.yaxis.axis_label = "Vuositulot"
    plot.yaxis[0].formatter = bm.NumeralTickFormatter(format="€0")


def get_categorical_stats_plot(df, *, category, value, na_as_category=None, line=True):
    df = get_categorical_stats(df, category, value, na_as_category=na_as_category)
    df = df.reset_index()
    df[category] = df[category].astype("category")
    plot = bp.figure(
        title=f"{category}/{value}",
        x_range=list(df[category].cat.categories),
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
    if line:
        plot.line(
            df[category],
            df["median"],
            legend_label="median",
            color="#1289A7",
            line_width=4,
        )
        plot.line(
            df[category],
            df["mean"],
            legend_label="mean",
            color="#B53471",
            line_width=4,
        )
    else:
        plot.circle(
            df[category],
            df["median"],
            radius=CAT_Q_RADIUS,
            legend_label="median",
            color="#1289A7",
        )
        plot.circle(
            df[category],
            df["mean"],
            radius=CAT_Q_RADIUS,
            legend_label="mean",
            color="#B53471",
        )
    return plot


def get_multiselect_frequency_plot(
    series: Series,
    *,
    title: str,
    top_n: int = 20,
) -> bp.figure:
    """Horizontal bar chart of the top N values from a comma-separated multiselect column."""
    counts = explode_multiselect(series, top_n=top_n)
    # Reverse so highest count is at the top
    labels = list(counts.index[::-1])
    values = list(counts.values[::-1])  # noqa: PD011

    plot = bp.figure(
        title=title,
        y_range=labels,
        height=max(300, 22 * len(labels)),
        width=700,
    )
    plot.hbar(y=labels, right=values, height=0.7, color="#2a6180")
    plot.xaxis.axis_label = "Vastauksia"
    plot.x_range.start = 0
    return plot
