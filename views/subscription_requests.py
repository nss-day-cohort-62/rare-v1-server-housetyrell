import sqlite3
from models import Subscription

def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
            FROM Subscriptions s
        """)
        subscriptions = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            subscriptions.append(subscription.__dict__)

    return subscriptions