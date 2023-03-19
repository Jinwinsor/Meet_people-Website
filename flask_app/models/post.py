from flask_app.config.mysqlconnection import connectToMySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.models import user, post, join
from flask_app.models.join import Joins
# from flask_app.models.user import User
from flask import flash


class Post:
    db = "meetyou"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.comment = data['comment']
        self.location = data['location']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.joins = []     # ONE post has MANY joins    **** MANY TO MANY
        # self.user = user
        self.owner = None


    # For preventing multiple joins.
    # If the user clicked the join button already, then no more. (same user_id)
    # def user_has_joined_post(self, user_id):
    #     for join in self.joins:
    #         if join.user_id == user.id:
    #             return False
    #     return True

    @classmethod
    def get_all_posts(cls):

        query = """
        SELECT * FROM posts
        LEFT JOIN users ON users.id = posts.user_id;
        
     
        """
        #    LEFT JOIN users ON joins.user_id = users.id;
        # SELECT * FROM posts
        # JOIN users ON users.id = posts.user_id
        # ORDER BY created_at DESC

        results = connectToMySQL(cls.db).query_db(query)
        print(" =================== ")
        print(results)
        print(" ============####### ")

        all_comments = []

        if not results:
            return []

        for row in results:
            # post.append(cls[row])
            this_post = cls(row)
            user_data = {
                'id': row['users.id'],     # posts.user_id = users.id
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }

            this_owner = user.User(user_data)
            this_post.owner = this_owner
            all_comments.append(this_post)

        return all_comments
        # =====================

    @classmethod
    def getOne_post(cls, data):
        query = """
        SELECT * FROM posts
        LEFT JOIN users
        ON posts.user_id = users.id
        LEFT JOIN joins
        ON joins.post_id = posts.id
        WHERE posts.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return None
        print(" =================== \n")
        print(results)
        print(" =================== \n")

        row = results[0]
        this_post = cls(results[0])

        user_data = {
            'id': row['users.id'],     # posts.user_id = users.id
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at'],
        }
        this_user = user.User(user_data)
        this_post.owner = this_user

        for rw in results:
            if not rw['joins.id'] == None:
                this_liker = user.User({
                    'id': rw['users.id'],
                    'first_name': rw['first_name'],
                    'last_name': rw['last_name'],
                    'email': rw['email'],
                    'password': rw['password'],
                    'created_at': rw['users.created_at'],
                    'updated_at': rw['users.updated_at']
                })
                this_post.joins.append(this_liker)
        return this_post

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO posts(title, comment, location, date, user_id)
        VALUES(%(title)s,%(comment)s, %(location)s, %(date)s, %(user_id)s);
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def getOne_user(cls, data):

        query = """
        SELECT * FROM posts
        LEFT JOIN joins ON posts.id = joins.post_id
        LEFT JOIN users ON joins.user_id = users.id
        WHERE id=%(id)s;
        """
        # query = """
        # SELECT * FROM posts
        # LEFT JOIN joins ON posts.id = joins.post_id
        # LEFT JOIN users ON joins.user_id = users.id
        # WHERE id=%(id)s;
        # """
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def update(cls, data):
        query = """
        UPDATE posts 
        SET title=%(title)s, comment=%(comment)s, location=%(location)s, date=%(date)s 
        WHERE id = %(id)s;
        """
        # AND user_id = %(user_id)s;
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM posts 
        WHERE id = %(id)s;
        """
        # AND user_id = %(user_id)s;
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod
    def valiate_comment(form):
        is_valid = True
        if len(form['title']) < 3:
            is_valid = False
            flash('Please add a title', 'create')
        if len(form['comment']) < 3:
            is_valid = False
            flash('Please add a comment', 'create')
        if len(form['location']) < 3:
            is_valid = False
            flash('Please add a location', 'create')
        if len(form['date']) < 3:
            is_valid = False
            flash('Please add  dates', 'create')
        return is_valid
