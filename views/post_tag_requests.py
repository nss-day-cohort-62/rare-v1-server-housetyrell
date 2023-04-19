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
        FROM posttags a
        """)

        post_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post_tag = Post_Tag(row['id'], row['post_id'], row['tag_id'])


            post_tags.append(post_tag.__dict__)

    return post_tags
def create_post_tag(new_post_tag):
    """sql create post_tag function"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO POSTTAGS
            (post_id, tag_id)
        VALUES
            (?);
        """, (new_post_tag['post_id'], new_post_tag['tag_id'], ))
        id = db_cursor.lastrowid
        new_post_tag['id'] = id
        return new_post_tag
