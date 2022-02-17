from unittest.mock import patch

from altair.utils.data import MaxRowsError
import pandas as pd
import pytest

from app import create_app
from app.database import get_db


@pytest.fixture
def app():
    app = create_app(config="testing")

    return app


@pytest.fixture
def test_client(app):
    with app.test_client() as test_client:
        return test_client


@pytest.fixture
def form_data():
    return {"depth_min": 500, "grad_min": 0.05}


@pytest.fixture
def well_coords():
    return [
        (35.8883487, -106.5795905, 1464.9, 0.16519898969212915),
        (35.8760489, -106.5867907, 2525.0, 0.12792079207920792),
    ]


@pytest.fixture
def well_coords_df():
    return pd.DataFrame({
        "latitude": [35.8883487, 35.8760489],
        "longitude": [-106.5795905, -106.5867907],
        "depth": [1464.9, 2525.0],
        "gradient": [0.16519898969212915, 0.12792079207920792],
    })


@pytest.fixture
def mock_query_db(well_coords):
    with patch("app.views.query_db") as mock:
        mock.return_value = well_coords

        yield mock


@pytest.fixture
def mock_plot_wells(well_coords):
    with patch("app.views.plot_wells") as mock:
        mock.side_effect = MaxRowsError

        yield mock


@pytest.fixture
def connection(app):
    with app.app_context():
        yield get_db()


@pytest.fixture
def depth_min():
    return 2000


@pytest.fixture
def grad_min():
    return 0.02
