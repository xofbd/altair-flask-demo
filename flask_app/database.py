import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
URI_DB = os.getenv('URI_DB')


def query_db(depth_min, grad_min):
    """Return wells that fit the search criteria."""
    engine = create_engine(URI_DB)

    query = text(
        """
        SELECT latitude, longitude, depth, gradient
        FROM wells
        WHERE depth > :depth_min and gradient > :grad_min
        """
    )

    with engine.connect() as conn:
        results = (
            conn
            .execute(query, depth_min=depth_min, grad_min=grad_min)
            .fetchall()
        )

    return results
