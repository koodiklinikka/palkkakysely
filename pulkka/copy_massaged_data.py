from pulkka.config import OUT_DIR
from pulkka.data_ingest import read_data


def main():
    df = read_data()
    df.to_html(OUT_DIR / "data.html", index=False)
    df.to_csv(OUT_DIR / "data.csv", index=False)
    df.to_excel(OUT_DIR / "data.xlsx", index=False)
    df.to_json(
        OUT_DIR / "data.json",
        orient="records",
        date_format="iso",
        force_ascii=False,
    )


if __name__ == "__main__":
    main()
