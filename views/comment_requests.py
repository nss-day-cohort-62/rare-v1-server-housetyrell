import json
import sqlite3
from models import Comment
def get_all_comments():
    """sql friendly function for getting all comments"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT c.id, c.post_id, c.author_id, c.content
        FROM Comments c
        """)
        comments = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])
            comments.append(comment.__dict__)
    return comments
def get_single_comment(id):
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT c.id, c.post_id, c.author_id, c.content
        FROM Comments c
            WHERE u.id = ? ;
        """, ( id,))
        data = db_cursor.fetchone()
        comment = Comment(data['id'], data['post_id'], data['author_id'], data['content'])
        return comment.__dict__

