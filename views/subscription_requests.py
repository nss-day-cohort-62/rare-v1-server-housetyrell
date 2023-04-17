import sqlite3
from models import Subscription

def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            FROM Subscriptions s
        """)

        # Initialize an empty list to hold all animal representations
        subscriptions = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            subscriptions.append(subscription.__dict__)

    return subscriptions