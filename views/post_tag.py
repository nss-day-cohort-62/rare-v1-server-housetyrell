import sqlite3
import json
from models import Post_Tag


def get_all_post_tags():
    """Method docstring."""
    with sqlite3.connect("./db.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.post_id,
            a.tag_id
        FROM post_tag a
        """)

        post_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post_tag = Post_Tag(row['id'], row['post_id'], row['tag_id'])

            post_tags.append(post_tag.__dict__)

    return post_tags
