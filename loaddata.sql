CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');


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
        ORDER BY p.publication_date ASC;


INSERT INTO `PostTags` VALUES(null, 1, 1);
INSERT INTO Tags ('label') VALUES ('Python');
INSERT INTO `PostTags` VALUES(null, 1, 2);
INSERT INTO `PostTags` VALUES(null, 2, 1);

INSERT INTO `Comments` VALUES (null, 1, 1, "I like this");
INSERT INTO `Comments` VALUES (null, 1, 3, "This is great");

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
            SELECT GROUP_CONCAT(a.content)
            FROM Comments a
            WHERE a.post_id = p.id
            ) as comments
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        LEFT OUTER JOIN PostTags pt ON pt.post_id = p.id
        LEFT OUTER JOIN Tags t ON pt.tag_id = t.id
        LEFT OUTER JOIN Comments a ON p.id = a.post_id
        WHERE p.id = 1



DELETE FROM PostTags
WHERE id > 5;


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
        WHERE p.id = 1

