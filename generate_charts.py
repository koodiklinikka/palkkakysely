import bokeh.plotting as bp
import bokeh.models as bm
import bokeh.layouts as bl
from pandas import DataFrame

from chart_utils import (
    gender_colormap,
    get_df_hover_tool,
    set_yaxis_cash,
    get_categorical_stats_plot,
)
from data_ingest import read_data

plot_funcs = set()


def plot_this(fn):
    """
    Decorator for marking a function as a plot generator.
    """
    plot_funcs.add(fn)


@plot_this
def plot_kokemus_tulot(df: DataFrame):
    source = bm.ColumnDataSource(df)
    plot = bp.figure(title="Kokemus/Vuositulot")
    plot.add_tools(get_df_hover_tool(df))
    plot.xaxis.axis_label = "Työkokemus (v)"
    set_yaxis_cash(plot)
    plot.circle(
        x="Työkokemus", y="Vuositulot", source=source, color=gender_colormap, size=10
    )
    return plot


@plot_this
def plot_ika_vuositulot(df: DataFrame):
    return get_categorical_stats_plot(df, category="Ikä", value="Vuositulot")


@plot_this
def plot_sukupuoli_vuositulot(df: DataFrame):
    return get_categorical_stats_plot(
        df, category="Sukupuoli", value="Vuositulot", na_as_category="EOS"
    )


def main():
    df = read_data()
    plots = [func(df) for func in sorted(plot_funcs, key=lambda f: f.__name__)]
    bp.output_file("out/charts.html", title="Koodiklinikan Palkkakysely")
    bp.save(bl.grid(plots, ncols=2))


if __name__ == "__main__":
    main()
