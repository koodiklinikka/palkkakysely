from data_ingest import read_data


def main():
    df = read_data()
    df.to_html("out/data.html", index=False)
    df.to_csv("out/data.csv", index=False)
    df.to_excel("out/data.xlsx", index=False)
    df.to_json(
        "out/data.json",
        orient="records",
        date_format="iso",
        force_ascii=False,
    )


if __name__ == "__main__":
    main()
