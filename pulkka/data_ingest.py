from __future__ import annotations

import hashlib
import re
import warnings

import numpy as np
import pandas as pd

from pulkka.column_maps import (
    BONUS_COL,
    COLUMN_MAP_2025,
    COMMISSION_COL,
    COMPANY_MAP,
    EQUITY_COL,
    EXPECTED_ROW_COUNT_2025,
    FEMALE_GENDER_VALUES,
    ID_COL,
    IDS_TO_DROP_2025,
    IKA_COL,
    KIKY_COL,
    KK_TULOT_COL,
    KK_TULOT_NORM_COL,
    KKPALKKA_COL,
    LAHITYO_COL,
    LOMARAHA_COL,
    MALE_GENDER_VALUES,
    NO_GENDER_VALUES,
    OTHER_GENDER_VALUES,
    PALVELUT_COL,
    ROLE_MAP,
    ROOLI_COL,
    ROOLI_NORM_COL,
    SUKUPUOLI_COL,
    TUNTILASKUTUS_ALV0_COL,
    TYOAIKA_COL,
    TYOKOKEMUS_COL,
    TYOPAIKKA_COL,
    VALUE_MAP_2025,
    VUOSILASKUTUS_ALV0_COL,
    VUOSITULOT_COL,
)
from pulkka.config import DATA_DIR, YEAR


def map_sukupuoli(r: pd.Series) -> str | None:  # Unused in 2025
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


def ucfirst(val) -> str:
    if isinstance(val, str):
        return val[0].upper() + val[1:]
    return val


def hash_row(r: pd.Series) -> str:
    source_data = (
        f"en.{int(r.Timestamp.timestamp() * 1000)}"  # NB (2025): hard-codes `en`!
    )
    return hashlib.sha256(source_data.encode()).hexdigest()[:16]


def read_initial_dfs() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(DATA_DIR / "data.xlsx")
    df.columns = df.columns.str.strip()

    if len(df) < EXPECTED_ROW_COUNT_2025:
        raise ValueError(
            f"Expected at least {EXPECTED_ROW_COUNT_2025} rows, got {len(df)}",
        )

    df = df[df["Timestamp"].notna()]  # Remove rows with no timestamp
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
    if YEAR != "2025":
        raise ValueError(
            "This code only works for 2025. "
            "Please use an older revision for older data.",
        )
    df = read_initial_dfs()

    df = df.rename(columns=COLUMN_MAP_2025)

    for col, val_map in VALUE_MAP_2025.items():
        df[col] = df[col].map(val_map).fillna(df[col]).astype("category")

    # Drop known bogus data
    df = df.drop(df[df[ID_COL].isin(IDS_TO_DROP_2025)].index)

    # Drop duplicate submissions: rows identical on all columns except
    # Timestamp and ID (keep the earliest submission)
    content_cols = [c for c in df.columns if c not in ("Timestamp", ID_COL)]
    before = len(df)
    df = df.sort_values("Timestamp").drop_duplicates(subset=content_cols, keep="first")
    n_dupes = before - len(df)
    if n_dupes:
        warnings.warn(f"Dropped {n_dupes} duplicate submission(s)")

    # Gender is already mapped via VALUE_MAP_2025
    df[SUKUPUOLI_COL] = df[SUKUPUOLI_COL].astype("category")
    df[IKA_COL] = df[IKA_COL].astype("category")
    df[KIKY_COL] = df[KIKY_COL].astype("category")

    # Working time is in h/week — normalize to fraction of 37.5h
    df[TYOAIKA_COL] = to_percentage(df[TYOAIKA_COL], 37.5)
    # Time in office is already a percentage
    df[LAHITYO_COL] = to_percentage(df[LAHITYO_COL], 100)

    # Try to clean up numbers with spaces, etc. to real numbers
    df[KKPALKKA_COL] = df[KKPALKKA_COL].apply(map_numberlike)
    df[TUNTILASKUTUS_ALV0_COL] = pd.to_numeric(
        df[TUNTILASKUTUS_ALV0_COL].apply(map_numberlike),
        errors="coerce",
    )
    df[VUOSILASKUTUS_ALV0_COL] = pd.to_numeric(
        df[VUOSILASKUTUS_ALV0_COL].apply(map_numberlike),
        errors="coerce",
    )

    # Synthesize Vuositulot from components:
    # (base_salary + commission) * 12 + lomaraha + bonus + equity
    for comp_col in [COMMISSION_COL, LOMARAHA_COL, BONUS_COL, EQUITY_COL]:
        df[comp_col] = pd.to_numeric(
            df[comp_col].apply(map_numberlike),
            errors="coerce",
        ).fillna(0)

    # Fold commission into monthly salary so KKPALKKA = base + commission
    df[KKPALKKA_COL] = (
        pd.to_numeric(df[KKPALKKA_COL], errors="coerce").fillna(0) + df[COMMISSION_COL]
    )

    base_yearly = df[KKPALKKA_COL] * 12
    lomaraha = df.get(LOMARAHA_COL, 0)
    bonus = df.get(BONUS_COL, 0)
    equity = df.get(EQUITY_COL, 0)

    df[VUOSITULOT_COL] = base_yearly + lomaraha + bonus + equity
    # If base salary is missing/zero, vuositulot should be NaN
    df.loc[
        pd.to_numeric(df[KKPALKKA_COL], errors="coerce").fillna(0) == 0,
        VUOSITULOT_COL,
    ] = np.nan

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


def to_percentage(ser: pd.Series, norm_max: float) -> pd.Series:
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


def force_age_numeric(df: pd.DataFrame) -> pd.DataFrame:
    age_map = {}
    for cat in df[IKA_COL].cat.categories:
        m = re.match(r"^(\d+)-(\d+)( v)?", cat)
        if m:
            age_map[cat] = int(round(float(m.group(1)) + float(m.group(2))) / 2)
    df[IKA_COL] = df[IKA_COL].apply(lambda r: age_map.get(r, r))
    return df


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


def main() -> None:
    pd.set_option("display.max_column", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_seq_items", None)
    pd.set_option("display.max_colwidth", 500)
    pd.set_option("expand_frame_repr", True)
    df = read_data()
    print(df.head())


if __name__ == "__main__":
    main()
