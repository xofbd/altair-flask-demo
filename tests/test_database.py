from pytest import approx, raises
from sqlalchemy.exc import ResourceClosedError

from app.database import close_connection, get_db, query_db


def assert_equal_list(list_1, list_2):
    """
    Assert that two lists are equal.

    Equal lists have the same length and if their values are floats, they are
    approximately equal to each other.
    """
    assert len(list_1) == len(list_2)

    compare(sorted(list_1), sorted(list_2))


def compare(val_1, val_2):
    if not isinstance(val_1, (int, float)):
        for x, y in zip(val_1, val_2):
            compare(x, y)
    elif isinstance(val_1, int):
        assert val_1 == val_2
    elif isinstance(val_1, float):
        assert val_1 == approx(val_2)


def test_query_db(connection, depth_min, grad_min):
    """
    GIVEN a connection to the database and depth and grad minimum
    WHEN query_db is called for those provided minimum values
    THEN the list of well data fitting the criteria is returned
    """
    results = query_db(connection, depth_min, grad_min)

    expected = [
        (29.2692, -97.0623, 3125.6, 0.0298502687484003),
        (33.2916, -95.6213, 2872.6, 0.0228364547796421),
        (27.3054, -97.3807, 3201.5, 0.0281118225831641),
        (42.9769, -116.2777, 2842.56, 0.0309580096814139),
        (32.1632, -95.081, 3597.6, 0.0279630865021125),
    ]

    assert_equal_list(results, expected)


def test_get_db(app):
    """
    GIVEN an application object
    WHEN a query made with the returned connection from get_db
    THEN the connection was not closed and a result is returned
    """
    with app.app_context():
        db = get_db()

        assert db.execute("SELECT 1").fetchall() == [(1,)]


def test_single_connection(app):
    """
    GIVEN an application object
    WHEN a get_db is called twice
    THEN the first, opened, connection is returned with a second call to get_db
    """
    with app.app_context():
        db = get_db()

        assert db is get_db()


def test_close_connection(connection):
    """
    GIVEN an open connection
    WHEN an exception is raised
    THEN the database connection is closed and no queries can be made
    """
    close_connection(Exception)

    with raises(ResourceClosedError) as e:
        connection.execute("SELECT 1")

    assert "This connection is closed" != str(e.value)
