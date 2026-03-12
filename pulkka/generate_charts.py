import bokeh.layouts as bl
import bokeh.models as bm
import bokeh.plotting as bp
from pandas import DataFrame

from pulkka.chart_utils import (
    gender_colormap,
    get_categorical_stats_plot,
    get_df_hover_tool,
    get_multiselect_frequency_plot,
    set_yaxis_cash,
)
from pulkka.column_maps import (
    IKA_COL,
    KAUPUNKI_COL,
    SUKUPUOLI_COL,
    TYOKOKEMUS_COL,
    VUOSITULOT_COL,
)
from pulkka.config import OUT_DIR
from pulkka.data_ingest import read_data

MULTISELECT_CHARTS = {
    "Data & ML": "Data & ML (top 15)",
    "DevOps & pilvi": "DevOps & pilvi (top 20)",
    "Edut (ei luontoisedut)": "Edut (top 15)",
    "Käyttöjärjestelmä": "Käyttöjärjestelmä",
    "Luontoisedut": "Luontoisedut (top 15)",
    "Ohjelmointikieli": "Ohjelmointikielet (top 20)",
    "Tietokannat": "Tietokannat (top 15)",
    "Web-kehykset": "Web-kehykset (top 20)",
}

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
    plot.scatter(
        x=TYOKOKEMUS_COL,
        y=VUOSITULOT_COL,
        source=source,
        color=gender_colormap,
        size=10,
    )
    return plot


@plot_this
def plot_ika_vuositulot(df: DataFrame):
    return get_categorical_stats_plot(df, category=IKA_COL, value=VUOSITULOT_COL)


@plot_this
def plot_sukupuoli_vuositulot(df: DataFrame):
    return get_categorical_stats_plot(
        df,
        category=SUKUPUOLI_COL,
        value=VUOSITULOT_COL,
        na_as_category="EOS",
    )


@plot_this
def plot_kaupunki_vuositulot(df: DataFrame):
    plot = get_categorical_stats_plot(
        df,
        category=KAUPUNKI_COL,
        value=VUOSITULOT_COL,
        line=False,
    )
    plot.xaxis.major_label_orientation = "vertical"
    return plot


def main():
    df = read_data()
    plots = [func(df) for func in sorted(plot_funcs, key=lambda f: f.__name__)]

    bp.output_file(OUT_DIR / "charts.html", title="Koodiklinikan Palkkakysely")
    bp.save(bl.grid(plots, ncols=2, sizing_mode="stretch_both"))

    multiselect_plots = []
    for col, title in MULTISELECT_CHARTS.items():
        if col in df.columns:
            top_n = 20 if "20" in title else 15
            multiselect_plots.append(
                get_multiselect_frequency_plot(df[col], title=title, top_n=top_n),
            )

    bp.output_file(
        OUT_DIR / "charts2.html",
        title="Koodiklinikan Palkkakysely – Monivalinnat",
    )
    bp.save(bl.grid(multiselect_plots, ncols=2, sizing_mode="stretch_both"))


if __name__ == "__main__":
    main()
