from __future__ import annotations

import hashlib
import re
import warnings

import numpy as np
import pandas
import pandas as pd

from pulkka.column_maps import (
    BOOLEAN_TEXT_TO_BOOLEAN_MAP,
    COLUMN_MAP_2024,
    COLUMN_MAP_2024_EN_TO_FI,
    COMPANY_MAP,
    EN_EXPECTED_ROW_COUNT,
    FEMALE_GENDER_VALUES,
    FI_EXPECTED_ROW_COUNT,
    ID_COL,
    IDS_TO_DROP,
    IKA_COL,
    KIKY_COL,
    KIKY_OTHER_COL,
    KK_TULOT_COL,
    KK_TULOT_NORM_COL,
    KKPALKKA_COL,
    LAHITYO_COL,
    LANG_COL,
    MALE_GENDER_VALUES,
    NO_GENDER_VALUES,
    OTHER_GENDER_VALUES,
    PALVELUT_COL,
    ROLE_MAP,
    ROOLI_COL,
    ROOLI_NORM_COL,
    SUKUPUOLI_COL,
    TYOAIKA_COL,
    TYOKOKEMUS_COL,
    TYOPAIKKA_COL,
    VALUE_MAP_2024_EN_TO_FI,
    VUOSITULOT_COL,
)
from pulkka.config import DATA_DIR, YEAR


def map_sukupuoli(r: pd.Series) -> str | None:
    value = r[SUKUPUOLI_COL]
    if not isinstance(value, str):
        return value

    value = value.lower()
    if (
        "nainen" in value
        or "female" in value
        or "woman" in value
        or value in FEMALE_GENDER_VALUES
    ):
        return "nainen"

    if value.strip() in MALE_GENDER_VALUES:
        return "mies"

    if value in NO_GENDER_VALUES:
        return None

    if value in OTHER_GENDER_VALUES:
        return "muu"

    raise NotImplementedError(f"Unknown sukupuoli: {value!r} (row ID {r[ID_COL]})")


def map_vuositulot(r):
    if r[VUOSITULOT_COL] is np.nan:
        return r[KKPALKKA_COL] * 12.5
    return r[VUOSITULOT_COL]


def map_numberlike(d):
    if isinstance(d, str):
        try:
            return float(re.sub(r"\s+", "", d))
        except ValueError:
            pass
    return d


def ucfirst(val):
    if isinstance(val, str):
        return val[0].upper() + val[1:]
    return val


def hash_row(r: pd.Series) -> str:
    source_data = f"{r[LANG_COL]}.{int(r.Timestamp.timestamp() * 1000)}"
    return hashlib.sha256(source_data.encode()).hexdigest()[:16]


def read_initial_dfs() -> pd.DataFrame:
    df_fi: pd.DataFrame = pd.read_excel(
        DATA_DIR / "results-fi.xlsx",
        skiprows=[1],  # Google Sheets exports one empty row
    )
    df_fi[LANG_COL] = "fi"

    if len(df_fi) < FI_EXPECTED_ROW_COUNT:
        raise ValueError(
            f"Expected at least {FI_EXPECTED_ROW_COUNT} rows in the Finnish data, got {len(df_fi)}",
        )

    df_en: pd.DataFrame = pd.read_excel(
        DATA_DIR / "results-en.xlsx",
        skiprows=[1],  # Google Sheets exports one empty row
    )
    df_en[LANG_COL] = "en"

    if len(df_fi) < EN_EXPECTED_ROW_COUNT:
        raise ValueError(
            f"Expected at least {EN_EXPECTED_ROW_COUNT} rows in the English data, got {len(df_en)}",
        )

    df_en = df_en.rename(columns=COLUMN_MAP_2024_EN_TO_FI)
    df = pd.concat([df_fi, df_en], ignore_index=True)
    df = df[df["Timestamp"].notna()]  # Remove rows with no timestamp
    df[LANG_COL] = df[LANG_COL].astype("category")
    # Give each row a unique hash ID
    df[ID_COL] = df.apply(hash_row, axis=1)
    # Ensure truncated sha is unique
    assert len(df[ID_COL].unique()) == len(df)
    return df


def map_case_insensitive(series: pd.Series, mapping: dict[str, str]) -> pd.Series:
    """
    Map a series of strings to another series of strings, case-insensitively.
    """
    lower_mapping = {k.lower(): v for k, v in mapping.items()}

    def map_value(v):
        if v is np.nan:
            return ""
        if not isinstance(v, str):
            raise TypeError(f"Unexpected value {v!r} of type {type(v)}")
        return lower_mapping.get(v.lower().strip(), v)

    return series.apply(map_value).fillna(series)


def read_data() -> pd.DataFrame:
    if YEAR != "2024":
        raise ValueError(
            "This code only works for 2024. "
            "Please use an older revision for older data.",
        )
    df = read_initial_dfs()

    df = df.rename(columns=COLUMN_MAP_2024)

    for col, val_map in VALUE_MAP_2024_EN_TO_FI.items():
        df[col] = df[col].map(val_map).fillna(df[col]).astype("category")

    # Drop known bogus data
    df = df.drop(df[df[ID_COL].isin(IDS_TO_DROP)].index)

    df[SUKUPUOLI_COL] = df.apply(map_sukupuoli, axis=1).astype("category")
    df[IKA_COL] = df[IKA_COL].astype("category")

    # Assume that people entering 37.5 (hours) as their työaika means 100%
    df.loc[df[TYOAIKA_COL] == 37.5, TYOAIKA_COL] = 100
    # Assume there is no actual 10x koodari among us
    df.loc[df[TYOAIKA_COL] == 1000, TYOAIKA_COL] = 100

    df[TYOAIKA_COL] = to_percentage(df[TYOAIKA_COL], 100)
    df[LAHITYO_COL] = to_percentage(df[LAHITYO_COL], 100)

    # Split out non-boolean answers from KIKY_COL to KIKY_OTHER_COL
    df = split_boolean_column_to_other(df, KIKY_COL, KIKY_OTHER_COL)

    # Try to clean up numbers with spaces, etc. to real numbers
    df[KKPALKKA_COL] = df[KKPALKKA_COL].apply(map_numberlike)
    df[VUOSITULOT_COL] = df[VUOSITULOT_COL].apply(map_numberlike)

    # Fix up Työpaikka
    df[TYOPAIKKA_COL] = df[TYOPAIKKA_COL].replace("-", np.nan)
    df[TYOPAIKKA_COL] = df[TYOPAIKKA_COL].replace(
        re.compile(r"\s+oy|oyj$", flags=re.I),
        "",
    )
    df[TYOPAIKKA_COL] = df[TYOPAIKKA_COL].map(COMPANY_MAP).fillna(df[TYOPAIKKA_COL])

    # Normalize initial capitalization in Rooli and Palvelut
    df[ROOLI_COL] = df[ROOLI_COL].apply(ucfirst)
    df[PALVELUT_COL] = df[PALVELUT_COL].apply(ucfirst)

    # Map Rooli via known roles
    df[ROOLI_NORM_COL] = map_case_insensitive(df[ROOLI_COL], ROLE_MAP)

    # Round työvuodet
    df[TYOKOKEMUS_COL] = df[TYOKOKEMUS_COL].round()

    # Fix known bogus data
    df = apply_fixups(
        df,
        [
            # ({ID_COL: "..."}, {VUOSITULOT_COL: 62000}),
        ],
    )
    # Fill in Vuositulot as 12.5 * Kk-tulot if empty
    df[VUOSITULOT_COL] = df.apply(map_vuositulot, axis=1)

    # Synthesize kk-tulot from Vuositulot
    df[KK_TULOT_COL] = pd.to_numeric(df[VUOSITULOT_COL], errors="coerce") / 12
    df[KK_TULOT_NORM_COL] = df[KK_TULOT_COL] / df[TYOAIKA_COL]

    return df


def to_percentage(ser: pandas.Series, norm_max: float) -> pandas.Series:
    """
    Convert a series of numbers to a percentage
    """
    ser = pd.to_numeric(ser, errors="coerce")
    if (
        norm_max * 0.7 > ser.max() > norm_max * 1.5
    ):  # check that we have a reasonable max value
        warnings.warn(f"Unexpected max value {ser.max()} in {ser.name}, {norm_max=}")
    ser = ser / norm_max
    return ser.clip(lower=0)


def split_boolean_column_to_other(df, col, other_col):
    df[col] = df[col].replace(BOOLEAN_TEXT_TO_BOOLEAN_MAP)
    df[other_col] = df[col].apply(
        lambda r: r if (r and not isinstance(r, bool)) else None,
    )
    df[col] = (
        df[col]
        .apply(
            lambda value: ["Ei", "Kyllä"][value]
            if isinstance(value, bool)
            else (np.nan if not value else "Muu"),
        )
        .astype("category")
    )
    # reorder columns so that other_col is right after col
    cols = list(df.columns)
    cols.remove(other_col)
    cols.insert(cols.index(col) + 1, other_col)
    df = df[cols]
    return df


def force_age_numeric(df):
    age_map = {}
    for cat in df[IKA_COL].cat.categories:
        m = re.match(r"^(\d+)-(\d+) v", cat)
        if m:
            age_map[cat] = int(round(float(m.group(1)) + float(m.group(2))) / 2)
    df[IKA_COL] = df[IKA_COL].apply(lambda r: age_map.get(r, r))
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


def apply_fixups(df: pd.DataFrame, fixups: list[tuple[dict, dict]]) -> pd.DataFrame:
    for match_cond, replace_cond in fixups:
        match_keys, match_values = zip(*match_cond.items())
        ix = df[list(match_keys)].eq(list(match_values)).all(axis=1)
        if not ix.any():
            raise ValueError(
                f"Fixup match condition {match_cond} did not match any rows",
            )
        replace_keys, replace_values = zip(*replace_cond.items())
        df.loc[ix, list(replace_keys)] = replace_values
    return df
