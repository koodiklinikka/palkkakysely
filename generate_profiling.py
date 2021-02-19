from data_ingest import read_data
from pandas_profiling import ProfileReport


def main():
    df = read_data()
    profile = ProfileReport(df)
    profile.to_file("out/profiling_report.html")


if __name__ == "__main__":
    main()
