from data_ingest import read_data


def main():
    df = read_data()
    df.to_html("out/data.html")
    df.to_csv("out/data.csv")
    df.to_excel("out/data.xlsx")


if __name__ == "__main__":
    main()
