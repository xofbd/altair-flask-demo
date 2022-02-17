#!/usr/bin/env python
"""
Create SQL table from an already existing database.
"""
import os

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()
URI = os.getenv("URI_DB")


def prepare_data(path_in, max_rows):
    """Wrangle and optionally truncate the data for SQL table."""
    T_surface = 20
    cols_to_drop = [
        "uuid",
        "name",
        "site_name",
        "other_location_name",
        "api",
        "shape",
        "precision_log_source_id",
    ]

    df = (
        pd.read_csv(path_in, dtype={"state_id": "Int32", "county_id": "Int32"})
        .assign(gradient=lambda df: (df["bht"] - T_surface) / df["depth"])
        .dropna(subset=["bht", "thermal_conductivity"], axis=0)
        .drop_duplicates(subset=["id"])
        .set_index("id")
        .drop(cols_to_drop, axis=1)
    )

    df_county, df_state, df_wells = normalize_data_frame(df)

    # We should only drop rows of the wells table
    if max_rows:
        rows_to_keep = max_rows - df_county.shape[0] - df_state.shape[0]
        df_wells = df_wells.sample(rows_to_keep, random_state=0)

    return df_county, df_state, df_wells


def create_table(**kwargs):
    """Create SQL tables from pandas data frame."""
    engine = create_engine(URI)

    for name, df in kwargs.items():
        df.to_sql(name, engine, if_exists="replace")

    # Since we'll query primarily based on depth and gradient, it makes
    # sense to create indices for these columns.
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX ix_depth ON wells(depth);"))
        conn.execute(text("CREATE INDEX ix_gradient ON wells(gradient);"))


def normalize_data_frame(df):
    """Normalize the data frame by splitting the data across 3 tables."""

    def _normalize(df, columns, col_index):
        return df[columns].drop_duplicates().dropna().set_index(col_index)

    df_county = _normalize(df, ["county_id", "county"], "county_id")
    df_state = _normalize(df, ["state_id", "state_code", "state"], "state_id")
    df_wells = df.drop(["county", "state", "state_code"], axis=1)

    return df_county, df_state, df_wells


def main(path_in, max_rows):
    dfs = prepare_data(path_in, max_rows)
    names = ("counties", "states", "wells")

    create_table(**dict(zip(names, dfs)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Create SQL database from a CSV file")
    parser.add_argument("path_in", help="Path to the CSV file")
    parser.add_argument(
        "--max_rows",
        type=int,
        help="If truncating, maximum number of rows to have across all tables ",
    )
    args = parser.parse_args()
    main(args.path_in, args.max_rows)
