import sqlite3
from models import Subscription

def get_all_subscriptions(query_params):
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        where_clause = ""
        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")
            if qs_key == "follower_id":
                where_clause = f"WHERE s.follower_id = {qs_value}"
            
        sql_to_execute = f"""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
            FROM Subscriptions s
            {where_clause}
        """
        db_cursor.execute(sql_to_execute)
        subscriptions = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            subscriptions.append(subscription.__dict__)

    return subscriptions

def create_subscription(new_subscription):
    """sql subscription creation"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO SUBSCRIPTIONS
            (follower_id, author_id, created_on)
        VALUES
            (?, ?, ?);
        """, (new_subscription['follower_id'], new_subscription['author_id'], new_subscription['created_on'] ))
        id = db_cursor.lastrowid
        new_subscription['id'] = id
        return new_subscription