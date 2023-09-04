import pandas as pd

from pulkka.column_maps import KKPALKKA_COL, VUOSITULOT_COL
from pulkka.config import OUT_DIR
from pulkka.data_ingest import read_data, force_age_numeric
from ydata_profiling import ProfileReport


def main():
    df = read_data()
    df[KKPALKKA_COL] = pd.to_numeric(df[KKPALKKA_COL], errors="coerce")
    df[VUOSITULOT_COL] = pd.to_numeric(df[VUOSITULOT_COL], errors="coerce")
    df = force_age_numeric(df)
    profile = ProfileReport(df)
    profile.config.vars.cat.n_obs = 20
    profile.to_file(OUT_DIR / "profiling_report.html")


if __name__ == "__main__":
    main()
