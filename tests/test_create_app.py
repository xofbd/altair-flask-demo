import pytest

from app import create_app


@pytest.mark.parametrize(
    'config, flask_env',
    [
        ('dev', 'development'),
        ('prod', 'production'),
        ('testing', 'testing'),
    ]
)
def test_create_app(config, flask_env):
    """
    GIVEN an application configuration
    WHEN create_app is called with a desired configuration
    THEN an app is returned with the correct configuration
    """
    assert create_app(config=config).config['FLASK_ENV'] == flask_env


def test_create_app_default():
    """
    GIVEN -
    WHEN create_app is called without any configuration
    THEN an app is returned with the default configuration
    """
    assert create_app().config['FLASK_ENV'] == 'development'


def test_no_testing_in_production():
    """
    GIVEN a configuration for production
    WHEN create_app is called for a production environment
    THEN the app does not have testing and debug enabled
    """
    assert not create_app(config='prod').testing
    assert not create_app(config='prod').debug
