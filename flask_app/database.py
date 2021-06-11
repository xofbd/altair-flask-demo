import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def query_db(depth_min, grad_min):
    """Return wells that fit the search criteria."""
    engine = create_engine(DATABASE_URL)

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
