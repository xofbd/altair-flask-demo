from bs4 import BeautifulSoup


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


def test_plot(test_client, form_data):
    """
    GIVEN a test client
    WHEN it makes a POST request to the plot page
    THEN the plot page is returned with the visualization
    """

    response = test_client.post('/plot', data=form_data)
    soup = create_soup(response)

    assert response.status_code
    assert 'Potential well sites' == soup.select_one('h2').text
    assert soup.select_one('div#vis > script')
