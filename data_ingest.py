import re

import numpy as np
import pandas as pd

COLUMN_MAP = {
    "Missä kaupungissa työpaikkasi pääasiallinen toimisto sijaitsee?": "Kaupunki",
    "Työaika (jos työsuhteessa)": "Työaika",
    "Etänä vai paikallisesti?": "Etä",
    "Vuositulot (sis. bonukset, osingot yms) / Vuosilaskutus (jos laskutat)": "Vuositulot",
    "Kuukausipalkka (jos työntekijä) (brutto)": "Kuukausipalkka",
    "Onko palkkasi nykyroolissasi mielestäsi kilpailukykyinen?": "Kilpailukykyinen",
}

ETATYO_MAP = {
    "Pääosin tai kokonaan etätyö": "Etä",
    "Pääosin tai kokonaan toimisto": "Toimisto",
    "Noin 50/50 hybridimalli": "50/50",
}


def map_sukupuoli(value: str):
    if isinstance(value, str):
        value = value.lower()
        if "nainen" in value or "female" in value:
            return "nainen"

        if (
            "mies" in value
            or "uros" in value
            or "miäs" in value
            or "äiä" in value
            or "male" in value
            or value == "m"
        ):
            return "mies"
        return "muu"  # Map the handful of outliers into "muu" (so a given value but not specified)
    return value


def map_vuositulot(r):
    if r["Vuositulot"] is np.nan:
        return r["Kuukausipalkka"] * 12.5
    return r["Vuositulot"]


def map_numberlike(d):
    if isinstance(d, str):
        try:
            return float(re.sub("\s+", "", d))
        except ValueError:
            pass
    return d


def read_data() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(
        "data/results.xlsx",
        skiprows=[1],  # Google Sheets exports one empty row
    )
    df.rename(columns=COLUMN_MAP, inplace=True)

    df["Kaupunki"].replace(
        "PK-Seutu (Helsinki, Espoo, Vantaa)", "PK-Seutu", inplace=True
    )
    df["Kaupunki"] = df["Kaupunki"].astype("category")
    df["Sukupuoli"] = df["Sukupuoli"].apply(map_sukupuoli).astype("category")
    df["Ikä"] = df["Ikä"].astype("category")

    df["Etä"] = df["Etä"].map(ETATYO_MAP).astype("category")
    df["Kilpailukykyinen"].replace({"Kyllä": True, "Ei": False}, inplace=True)

    # Try to clean up numbers with spaces, etc. to real numbers
    df["Kuukausipalkka"] = df["Kuukausipalkka"].apply(map_numberlike)
    df["Vuositulot"] = df["Vuositulot"].apply(map_numberlike)

    # Fill in Vuositulot as 12.5 * Kk-tulot if empty
    df["Vuositulot"] = df.apply(map_vuositulot, axis=1)
    return df


def main():
    pd.set_option("display.max_column", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_seq_items", None)
    pd.set_option("display.max_colwidth", 500)
    pd.set_option("expand_frame_repr", True)
    df = read_data()
    print(df.head())


if __name__ == "__main__":
    main()
