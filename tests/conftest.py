import pytest

from app.app import app


@pytest.fixture
def test_client():
    with app.test_client() as test_client:
        return test_client


@pytest.fixture
def form_data():
    return {'depth_min': 500, 'grad_min': 0.05}
