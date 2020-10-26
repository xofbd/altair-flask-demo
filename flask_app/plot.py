import os
import sqlite3

import altair as alt
import pandas as pd
from vega_datasets import data


def query_db(depth_min, grad_min):
    """Return well data given minimum depth and gradient."""
    conn = sqlite3.connect(os.path.join('data', 'wells.db'))
    cursor = conn.cursor()

    query = """
    SELECT latitude, longitude, depth, gradient
    FROM wells
    WHERE depth > ? and gradient > ?
    """
    data = cursor.execute(query, (depth_min, grad_min)).fetchall()
    conn.close()

    return data


def plot_wells(well_coords):
    """Return JSON of Altair chart."""

    # Process data
    counties = alt.topo_feature(data.us_10m.url, 'counties')
    columns = ['latitude', 'longitude', 'depth', 'gradient']
    well_coords = pd.DataFrame(well_coords, columns=columns)

    # Create charts
    selection = alt.selection_interval(bind='scales')

    map_ = (alt.Chart(counties)
            .mark_geoshape(fill='lightgray', stroke='white')
            .properties(width=500, height=500)
            .project('albersUsa'))

    well_locations = (alt.Chart(well_coords)
                      .mark_circle()
                      .encode(longitude='longitude:Q',
                              latitude='latitude:Q',
                              tooltip=['depth:Q', 'gradient:Q'],
                              color=alt.value('steelblue')))

    chart = map_ + well_locations

    return chart.to_json()
