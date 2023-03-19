from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_app.models import post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "meetyou"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []  # self.joined_posts   / ONE user has MANY posts

    @classmethod
    def get_all_user(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users(first_name,last_name,email,password) 
        VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def getOneByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def getOne(cls, data):
        query = """
        SELECT * FROM users 
        LEFT JOIN posts ON users.id = posts.user_id 
        WHERE users.id = %(id)s
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        if results:
            this_user = cls(results[0])
            print("This is the results======")
            print(results)
            print("this is the results[0] #######")
            print(results[0])
            for row in results:
                if row['user_id'] == None:  # user_id ==> posts.user_id
                    break

                # One user has many posts
                this_user.posts.append(post.Post(row))

            # If there is something, then add the value in the post.Post. and then return to this_user.
            return this_user
        return False   # If no results exists , I can return it False

    @staticmethod
    def validate_user(data):
        is_valid = True

        # Check no empty input
        if len(data['first_name']) < 1 or len(data['last_name']) < 1 or len(data['email']) < 1:
            flash("Please fill out your informtaion", "register")
            is_valid = False

        # Check right email format
        if len(data['email']) > 1 and not EMAIL_REGEX.match(data['email']):
            flash("Invalid email format!", "register")
            is_valid = False

        # Check passwords are matched
        if data['password'] != data['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False

        if data['password'] == '':
            flash("Please enter password", "register")
            is_valid = False
        return is_valid

    @classmethod
    def dontJoin_users(cls, data):
        query = """
        SELECT * FROM users WHERE users.id 
        NOT IN ( SELECT user_id FROM joins 
        WHERE post_id = %(id)s );
        """
        users = []
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            users.append(cls(row))
        print(users)
        return users
