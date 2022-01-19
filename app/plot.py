import altair as alt
import pandas as pd
from vega_datasets import data


def plot_wells(well_coords):
    """Return JSON of Altair chart."""

    # Process data
    counties = alt.topo_feature(data.us_10m.url, 'counties')
    columns = ['latitude', 'longitude', 'depth', 'gradient']
    well_coords = pd.DataFrame(well_coords, columns=columns)

    # Create charts
    map_ = (
        alt.Chart(counties)
        .mark_geoshape(fill='lightgray', stroke='white')
        .properties(width=500, height=500)
        .project('albersUsa')
    )

    well_locations = (
        alt.Chart(well_coords)
        .mark_circle()
        .encode(
            longitude='longitude:Q',
            latitude='latitude:Q',
            color=alt.Color('gradient:Q', scale=alt.Scale(scheme='inferno')),
            tooltip=[
                alt.Tooltip('depth:Q', title='Depth (m)', format='d'),
                alt.Tooltip(
                    'gradient:Q',
                    title='Gradient (°C/m)',
                    format='0.2f'
                ),
            ]
        )
    )

    chart = map_ + well_locations

    return chart.to_json()
