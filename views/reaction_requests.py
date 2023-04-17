import sqlite3
import json
from models import Reaction


def get_all_reactions():
    """Method docstring."""
    with sqlite3.connect("./db.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.image_url
        FROM reactions a
        """)

        reactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            reaction = Reaction(row['id'], row['image_url'])

            reactions.append(reaction.__dict__)

    return reactions
    