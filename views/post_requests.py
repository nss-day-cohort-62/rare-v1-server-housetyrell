import json
import sqlite3
from models import Post, Category, User, Comment
from .tag_requests import get_single_tag
from .comment_requests import get_single_comment

def get_all_posts(query_params):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        cat_where_clause = None
        user_where_clause = None
        tag_where_clause = None
        if len(query_params) != 0:
            if query_params.get("category_id"):
                cat_where_clause = f"p.category_id = {query_params['category_id'][0]}"
            if query_params.get("user_id"):
                user_where_clause = f"p.user_id = {query_params['user_id'][0]}"
            if query_params.get("tag_id"):
                tag_where_clause = f"t.id = {query_params['tag_id'][0]}"
        full_where_clause = ""
        if (cat_where_clause or user_where_clause or tag_where_clause):
            joined_tuple = [cat_where_clause, user_where_clause, tag_where_clause]
            new_tuple = []
            for item in joined_tuple:
                if item is not None:
                    new_tuple.append(item)
            full_joined_tuple = " AND ".join(new_tuple)
            full_where_clause = f"WHERE {full_joined_tuple}"
            print(full_where_clause)
    sql_to_execute = f"""
        SELECT DISTINCT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            p.approved,
            p.image_url,
            u.first_name user_first_name,
            u.last_name user_last_name,
            u.email user_email,
            u.bio user_bio,
            u.username user_username,
            u.password user_password,
            u.profile_image_url user_profile_image_url,
            u.created_on user_created_on,
            u.active user_active,
            c.label category_label,
            (
            SELECT GROUP_CONCAT(t.id)
            FROM PostTags pt JOIN Tags t ON pt.tag_id = t.id
            WHERE pt.post_id = p.id
            ) as post_tags
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        LEFT OUTER JOIN PostTags pt ON pt.post_id = p.id
        LEFT OUTER JOIN Tags t ON pt.tag_id = t.id
        {full_where_clause}
        ORDER BY p.publication_date ASC
        """
    db_cursor.execute(sql_to_execute)
    posts = []
    dataset = db_cursor.fetchall()
    for row in dataset:
        post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                    row['publication_date'], row['image_url'], row['content'], row['approved'])
        category = Category(row['category_id'], row['category_label'])
        user = User(row['user_id'], row['user_first_name'], row['user_last_name'], row['user_email'],
                    row['user_bio'], row['user_username'], row['user_password'],
                    row['user_profile_image_url'], row['user_created_on'], row['user_active'])
        post_tags = row['post_tags'].split(',') if row['post_tags'] else []
        post_with_tags = []
        for post_tag in post_tags:
            tag_object = get_single_tag(post_tag)
            post_with_tags.append(tag_object)
        post.post_tags = post_with_tags
        post.user = user.__dict__
        post.category = category.__dict__
        posts.append(post.__dict__)
    return posts


def get_single_posts(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

    db_cursor.execute("""
        SELECT DISTINCT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            p.approved,
            p.image_url,
            u.first_name user_first_name,
            u.last_name user_last_name,
            u.email user_email,
            u.bio user_bio,
            u.username user_username,
            u.password user_password,
            u.profile_image_url user_profile_image_url,
            u.created_on user_created_on,
            u.active user_active,
            c.label category_label,
            (
            SELECT GROUP_CONCAT(t.id)
            FROM PostTags pt JOIN Tags t ON pt.tag_id = t.id
            WHERE pt.post_id = p.id
            ) as post_tags,
            (
            SELECT GROUP_CONCAT(a.id)
            FROM Comments a
            WHERE a.post_id = p.id
            ) as comments
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        LEFT OUTER JOIN PostTags pt ON pt.post_id = p.id
        LEFT OUTER JOIN Tags t ON pt.tag_id = t.id
        LEFT OUTER JOIN Comments a ON p.id = a.post_id
        WHERE p.id = ?;
        """, (id, ))

    data = db_cursor.fetchone()

    post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                data['publication_date'], data['image_url'], data['content'], data['approved'])
    category = Category(data['category_id'], data['category_label'])
    user = User(data['user_id'], data['user_first_name'], data['user_last_name'], data['user_email'],
                data['user_bio'], data['user_username'], data['user_password'],
                data['user_profile_image_url'], data['user_created_on'], data['user_active'])
    post_tags = data['post_tags'].split(',') if data['post_tags'] else []
    post_with_tags = []
    for post_tag in post_tags:
        tag_object = get_single_tag(post_tag)
        post_with_tags.append(tag_object)
    comments = data['comments'].split(",") if data['comments'] else []
    post_with_comments = []
    for comment in comments:
        comment_object = get_single_comment(comment)
        post_with_comments.append(comment_object)
    post.comments = post_with_comments
    post.post_tags = post_with_tags
    post.user = user.__dict__
    post.category = category.__dict__
    
    return post.__dict__


def get_post_by_search(search):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            p.approved,
            p.image_url,
            u.first_name user_first_name,
            u.last_name user_last_name,
            u.email user_email,
            u.bio user_bio,
            u.username user_username,
            u.password user_password,
            u.profile_image_url user_profile_image_url,
            u.created_on user_created_on,
            u.active user_active,
            c.label category_label
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.title LIKE ?;
        """, ( f"%{search}%", ))
        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                row['publication_date'], row['image_url'], row['content'], row['approved'])
            posts.append(post.__dict__)
        return posts

def create_post(new_post):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT * 
            FROM Posts p
            LEFT OUTER JOIN PostTags pt 
                ON p.id = pt.post_id
            LEFT OUTER JOIN Tags t
                ON pt.tag_id = t.id
        """)
        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved']))
        id = db_cursor.lastrowid
        new_post['id'] = id
        print(new_post['post_tags'])
        for tag in new_post['post_tags']:
            db_cursor.execute("""
            INSERT INTO PostTags
                (post_id, tag_id)
            VALUES
                (?, ?)
            """, (new_post['id'], tag, ))

        return new_post



def update_post(id, new_post):
    """Method docstring."""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?;
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'], id, ))
# NOT DEFINING NEW_POST['ID'] ON LINE 250
        for tag in new_post['post_tags']:
            db_cursor.execute("""
                DELETE FROM PostTags pt
                WHERE pt.post_id = ?;
                """, (new_post['id'], ))
        for tag in new_post['post_tags']:
            db_cursor.execute("""
                INSERT INTO PostTags
                    (post_id, tag_id)
                VALUES
                    (?, ?);
                """, (new_post['id'], tag))
    rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def delete_post(id):
    "deleting an order"
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))
