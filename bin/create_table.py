#!/usr/bin/env python
"""
Create SQL table from an already existing database.
"""
import os

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
URI = os.getenv('URI')
NUM_ROWS = 10_000


def truncate_data(path_in):
    """Truncate data for SQL table due to Heroku hobby tier."""
    T_surface = 20

    return (
        pd.read_csv(path_in)
        .assign(gradient=lambda df: (df['bht'] - T_surface) / df['depth'])
        .dropna(subset=['bht', 'thermal_conductivity'], axis=0)
        .drop_duplicates(subset=['id'])
        .sample(NUM_ROWS, random_state=0)
    )


def create_table(df):
    """Create SQL table from pandas data frame."""
    engine = create_engine(URI)

    df.to_sql('wells', engine)


def main(path_in):
    df = truncate_data(path_in)
    create_table(df)


if __name__ == '__main__':
    import sys

    main(sys.argv[1])
