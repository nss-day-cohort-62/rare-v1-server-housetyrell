import json
import sqlite3
from models import Post_reaction
def get_all_post_reactions():
    """sql friendly function for getting all post reactions"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT pr.id, pr.user_id, pr.reaction_id, pr.post_id
        FROM PostReactions pr
        """)
        post_reactions = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post_reaction = Post_reaction(row['id'], row['user_id'], row['reaction_id'], row['post_id'])
            post_reactions.append(post_reaction.__dict__)
    return post_reactions
