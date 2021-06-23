#!/usr/bin/env python
"""
Create SQL table from an already existing database.
"""
import os

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
URI = os.getenv('URI_DB')


def truncate_data(path_in, truncate):
    """Truncate data for SQL table due to Heroku hobby tier."""
    T_surface = 20

    df = (
        pd.read_csv(path_in)
        .assign(gradient=lambda df: (df['bht'] - T_surface) / df['depth'])
        .dropna(subset=['bht', 'thermal_conductivity'], axis=0)
        .drop_duplicates(subset=['id'])
    )

    if truncate is None:
        return df
    else:
        return df.sample(truncate, random_state=0)


def create_table(df):
    """Create SQL table from pandas data frame."""
    engine = create_engine(URI)

    df.to_sql('wells', engine)


def main(path_in, truncate):
    df = truncate_data(path_in, truncate)
    create_table(df)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("Create SQL database from a CSV file")
    parser.add_argument('path_in', help="Path to the CSV file")
    parser.add_argument(
        '--truncate',
        type=int,
        help="If truncating, how many rows to keep in the table"
    )
    args = parser.parse_args()
    main(args.path_in, args.truncate)
