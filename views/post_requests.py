import json
import sqlite3
from models import Post, Category, User


def get_all_posts():
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
        ORDER BY p.publication_date ASC;
        """)
    posts = []
    dataset = db_cursor.fetchall()
    for row in dataset:
        post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                    row['publication_date'], row['image_url'], row['content'], row['approved'])
        category = Category(row['category_id'], row['category_label'])
        user = User(row['user_id'], row['user_first_name'], row['user_last_name'], row['user_email'],
                    row['user_bio'], row['user_username'], row['user_password'],
                    row['user_profile_image_url'], row['user_created_on'], row['user_active'])

        post.user = user.__dict__
        post.category = category.__dict__
        posts.append(post.__dict__)
    return posts


def get_single_posts(id):
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
        WHERE p.id = ?;
        """, (id, ))

    data = db_cursor.fetchone()

    post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                data['publication_date'], data['image_url'], data['content'], data['approved'])
    category = Category(data['category_id'], data['category_label'])
    user = User(data['user_id'], data['user_first_name'], data['user_last_name'], data['user_email'],
                data['user_bio'], data['user_username'], data['user_password'],
                data['user_profile_image_url'], data['user_created_on'], data['user_active'])

    post.user = user.__dict__
    post.category = category.__dict__
    return post.__dict__


# def get_posts_for_current_user(user_id):
#     """sql function for getting posts for active user"""
#     with sqlite3.connect('./db.sqlite3') as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()
#         db_cursor.execute("""
#         SELECT
#             p.id,
#             p.user_id,
#             p.category_id,
#             p.title,
#             p.publication_date,
#             p.content,
#             p.approved,
#             p.image_url,
#             u.first_name user_first_name,
#             u.last_name user_last_name,
#             u.email user_email,
#             u.bio user_bio,
#             u.username user_username,
#             u.password user_password,
#             u.profile_image_url user_profile_image_url,
#             u.created_on user_created_on,
#             u.active user_active,
#             c.label category_label
#         FROM Posts p
#         WHERE p.user_id = ?
#         JOIN Users u ON u.id = p.user_id
#         JOIN Categories c ON c.id = p.category_id
#         ORDER BY p.publication_date ASC;
#         """, (user_id, ))
#         posts = []
#         dataset = db_cursor.fetchall()
#         for row in dataset:
#             post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
#                         row['publication_date'], row['image_url'], row['content'], row['approved'])
#             category = Category(row['id'], row['category_label'])
#             user = User(row['id'], row['user_first_name'], row['user_last_name'], row['user_email'],
#                         row['user_bio'], row['user_username'], row['user_password'],
#                         row['user_profile_image_url'], row['user_created_on'], row['user_active'])

#             post.user = user.__dict__
#             post.category = category.__dict__
#             posts.append(post.__dict__)
#         return posts



def create_post(new_post):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved']))

        id = db_cursor.lastrowid
        new_post['id'] = id
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
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'], id, ))

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
