from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash 
import re

# Validation schematics
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Post:
    def __init__(self ,data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creater = None

    @classmethod
    def get_all_posts_with_creator(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL('twitter').query_db(query)
        print("These are the results:", results)
        all_posts_creater = []
        for item in results:
            user_info_for_posts = cls(item)
            one_creaters_info = {
            "id": item['users.id'],
            "first_name": item['first_name'],
            "last_name": item['last_name'],
            "email": item['email'],
            "password": item['password'],
            "created_at": item['created_at'],
            "updated_at": item['updated_at']
            }
            user_info_for_posts.creater = user.User(one_creaters_info)
            all_posts_creater.append(user_info_for_posts)
            # print("This is the creator:", post.creater.first_name)
        # print("These are all the posts", all_posts_creater)
        return all_posts_creater


    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, created_at, updated_at, user_id) VALUES ( %(content)s , NOW() , NOW() , %(user_id)s );"
        return connectToMySQL('twitter').query_db( query, data )

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
    #     print(query)
    #     return connectToMySQL('twitter').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL('twitter').query_db( query, data )
