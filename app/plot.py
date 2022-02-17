import altair as alt
import pandas as pd
from vega_datasets import data


def process_data(well_coords):
    """Return pandas DataFrame of queried well data"""
    columns = ["latitude", "longitude", "depth", "gradient"]

    return pd.DataFrame(well_coords, columns=columns)


def plot_map():
    """Return Altair Chart of map of the USA"""
    counties = alt.topo_feature(data.us_10m.url, "counties")

    return (
        alt.Chart(counties)
        .mark_geoshape(fill="lightgray", stroke="white")
        .properties(width=500, height=500)
        .project("albersUsa")
    )


def plot_locations(well_coords):
    """Return Altair Chart of queried well locations"""

    return (
        alt.Chart(well_coords)
        .mark_circle()
        .encode(
            longitude="longitude:Q",
            latitude="latitude:Q",
            color=alt.Color("gradient:Q", scale=alt.Scale(scheme="inferno")),
            tooltip=[
                alt.Tooltip("depth:Q", title="Depth (m)", format="d"),
                alt.Tooltip(
                    "gradient:Q",
                    title="Gradient (°C/m)",
                    format="0.2f"
                ),
            ]
        )
    )


def plot_wells(well_coords):
    """Return Vega-Lite JSON of map of USA with queried wells"""
    well_coords = process_data(well_coords)
    map_ = plot_map()
    well_locations = plot_locations(well_coords)

    return (map_ + well_locations).to_json()
