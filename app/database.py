from flask import current_app as app, g
from sqlalchemy import create_engine, text


def get_db():
    """Return connection to the database"""
    db = getattr(g, '_database', None)

    if db is None:
        engine = create_engine(app.config['URI_DB'])
        g._database = engine.connect()

    return g._database


def close_connection(exception):
    """Close connection to the database"""
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


def init_app(app):
    """Close any open connections of the application context"""
    app.teardown_appcontext(close_connection)


def query_db(conn, depth_min, grad_min):
    """Return wells that fit the search criteria."""
    query = text(
        """
        SELECT latitude, longitude, depth, gradient
        FROM wells
        WHERE depth > :depth_min AND gradient > :grad_min;
        """
    )

    return (
        conn
        .execute(query, depth_min=depth_min, grad_min=grad_min)
        .fetchall()
    )
