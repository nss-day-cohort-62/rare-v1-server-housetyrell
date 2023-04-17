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
            a.emoji
        FROM reaction a
        """)

        reactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            reaction = Reaction(row['id'], row['emoji'])

            reactions.append(reaction.__dict__)

    return reactions
    