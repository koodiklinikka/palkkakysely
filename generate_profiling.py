from data_ingest import read_data, force_tulot_numeric, force_age_numeric
from pandas_profiling import ProfileReport


def main():
    df = read_data()
    df = force_tulot_numeric(df)
    df = force_age_numeric(df)
    profile = ProfileReport(df)
    profile.to_file("out/profiling_report.html")


if __name__ == "__main__":
    main()
