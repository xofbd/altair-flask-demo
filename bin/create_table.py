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


def prepare_data(path_in, truncate):
    """Wrangle and optionally truncate the data for SQL table."""
    T_surface = 20
    cols_to_drop = [
        'uuid', 'name', 'site_name', 'other_location_name', 'api', 'shape',
        'precision_log_source_id'
    ]

    df = (
        pd.read_csv(path_in, dtype={'state_id': 'Int32', 'county_id': 'Int32'})
        .assign(gradient=lambda df: (df['bht'] - T_surface) / df['depth'])
        .dropna(subset=['bht', 'thermal_conductivity'], axis=0)
        .drop_duplicates(subset=['id'])
        .set_index('id')
        .drop(cols_to_drop, axis=1)
    )

    if truncate:
        return df.sample(truncate, random_state=0)
    else:
        return df


def create_table(df):
    """Create SQL table from pandas data frame."""
    engine = create_engine(URI)

    df.to_sql('wells', engine)


def main(path_in, truncate):
    df = prepare_data(path_in, truncate)
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
