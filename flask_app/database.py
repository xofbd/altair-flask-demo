import os
import sqlite3

from flask import g

DATABASE = os.path.join('data', 'wells.db')


def get_db():
    """Return database connection object"""
    try:
        return g._database
    except AttributeError:
        g._database = sqlite3.connect(DATABASE)
        return g._database


def close_connection(exception):
    """Close database connection."""
    try:
        g._database.close()
    except AttributeError:
        pass


def query_db(depth_min, grad_min):
    """Return well data given minimum depth and gradient."""
    cursor = get_db().cursor()
    query = """
    SELECT latitude, longitude, depth, gradient
    FROM wells
    WHERE depth > ? and gradient > ?
    """

    return cursor.execute(query, (depth_min, grad_min)).fetchall()
