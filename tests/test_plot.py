import json

from app.plot import plot_locations, plot_map, plot_wells, process_data


def is_vega_lite_json(json_string):
    """Return True if JSON string is a Vega-Lite JSON specification"""

    return "vega-lite" in json.loads(json_string)["$schema"]


def test_process_data(well_coords, well_coords_df):
    """
    GIVEN a list of well coordinates
    WHEN process_data function is called
    THEN the well coordinates are converted into a pandas DataFrame
    """

    assert (process_data(well_coords) == well_coords_df).values.all()


def test_plot_map():
    """
    GIVEN -
    WHEN the returned Altair Chart object from calling plot_map is converted
    into a JSON
    THEN the resulting JSON is Vega-Lite JSON
    """

    assert is_vega_lite_json(plot_map().to_json())


def test_plot_locations(well_coords_df):
    """
    GIVEN a DataFrame of well coordinates
    WHEN the returned Altair Chart object from calling plot_locations is
    converted into a JSON
    THEN the resulting JSON is Vega-Lite JSON
    """

    assert is_vega_lite_json(plot_locations(well_coords_df).to_json())


def test_plot_wells(well_coords):
    """
    GIVEN a list of well coordinates
    WHEN plot_wells is called
    THEN a Vega-Lite JSON is returned with two layers
    """

    assert len(json.loads(plot_wells(well_coords))["layer"]) == 2
