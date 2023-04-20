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
            WHERE c.id = ? ;
        """, ( id,))
        data = db_cursor.fetchone()
        comment = Comment(data['id'], data['post_id'], data['author_id'], data['content'])
        return comment.__dict__
    
def create_comment(new_comment):
    """sql create comment"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Comments
            (author_id, post_id, content)
        VALUES
            (?, ?, ?);
        """, (new_comment['author_id'], new_comment['post_id'], new_comment['content']))
        id = db_cursor.lastrowid
        new_comment['id'] = id
        return new_comment
    
def delete_comment(id):
    """Method docstring."""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))
