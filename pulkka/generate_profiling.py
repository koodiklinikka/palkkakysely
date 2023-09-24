from pulkka.config import OUT_DIR
from pulkka.data_ingest import read_data, force_tulot_numeric, force_age_numeric
from ydata_profiling import ProfileReport


def main():
    df = read_data()
    df = force_tulot_numeric(df)
    df = force_age_numeric(df)
    profile = ProfileReport(df)
    profile.config.vars.cat.n_obs = 20
    profile.to_file(OUT_DIR / "profiling_report.html")


if __name__ == "__main__":
    main()
