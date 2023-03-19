
from flask_app.config.mysqlconnection import connectToMySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.models import user, post
from flask import flash
from flask_app.models.user import User
db = "meetyou"


class Joins:

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']

    @classmethod
    def count_likes(cls, post_id):
        query = "SELECT COUNT(*) FROM joins WHERE post_id = %(post_id)s"
        result = connectToMySQL(db).query_db(query, {'post_id': post_id})
        return result[0]['COUNT(*)']

    @classmethod
    def every_likes(cls, post_id):
        query = "SELECT * FROM joins WHERE post_id = %(post_id)s;"
        result = connectToMySQL(db).query_db(query, {'post_id': post_id})
        return result

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO joins
        (user_id, post_id)
        VALUES
        (%(user_id)s, %(post_id)s);
        """
        result = connectToMySQL("meetyou").query_db(query, data)
        return result

    @classmethod
    def leave(cls, data):
        query = """
        DELETE FROM joins 
        WHERE user_id = %(user_id)s AND post_id = %(post_id)s;
        """
        result = connectToMySQL("meetyou").query_db(query, data)
        return result

    @classmethod
    def user_dont_like(cls, data):
        query = """
        SELECT * FROM posts WHERE posts.id
        NOT IN ( SELECT post_id FROM joins
        WHERE user_id = %(id)s );
        """
        # This post has never had join from this user
        posts = []
        results = connectToMySQL("meetyou").query_db(query, data)
        if results:
            for row in results:
                posts.append(cls(row))
            return posts
        else:
            False
# ===================

    @classmethod
    def get_users_by_post_id(cls, post_id):
        query = """
        SELECT users.* FROM users
        JOIN joins ON users.id = joins.user_id
        WHERE joins.post_id = %(post_id)s;
        """
        results = connectToMySQL(db).query_db(query, {'post_id': post_id})
        users = []
        for row in results:
            users.append(User(row))
        return users
