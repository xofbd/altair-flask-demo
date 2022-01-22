from bs4 import BeautifulSoup
import pytest


def create_soup(response):
    """Return Beautiful Soup from parsing response object"""
    return BeautifulSoup(response.data, 'html.parser')


def test_index(test_client):
    """
    GIVEN a test client
    WHEN it makes a GET request to the index page
    THEN the index page is returned with the form
    """
    response = test_client.get('/')
    soup = create_soup(response)

    assert response.status_code == 200
    assert 'Enter the well criteria' == soup.select_one('h2').text
    assert soup.select_one('form')


def test_plot(test_client, form_data, mock_query_db):
    """
    GIVEN a test client and a mocked query_db function
    WHEN it makes a POST request to /
    THEN a page is returned with the visualization
    """
    response = test_client.post('/', data=form_data)
    soup = create_soup(response)

    mock_query_db.assert_called_once()
    assert response.status_code
    assert soup.select_one('h2').text == 'Potential well sites'
    assert soup.select_one('div#vis > script')


@pytest.mark.parametrize(
    'form_data_invalid, error_message',
    [
        ({'depth_min': -1, 'grad_min': 0.05}, 'Number must be at least 0.'),
        ({'depth_min': '', 'grad_min': 0.05}, 'This field is required.'),
        ({'depth_min': 500, 'grad_min': -1}, 'Number must be at least 0.'),
        ({'depth_min': 500, 'grad_min': ''}, 'This field is required.'),
    ]
)
def test_invalid_input(test_client, form_data_invalid, error_message):
    """
    GIVEN a test client
    WHEN it makes a POST request to / with invalid data
    THEN the index page is reloaded with invalid feedback message
    """
    response = test_client.post('/', data=form_data_invalid)
    soup = create_soup(response)

    assert response.status_code == 200
    assert soup.select_one('h2').text == 'Enter the well criteria'
    assert soup.select_one('.invalid-feedback').text.strip() == error_message
