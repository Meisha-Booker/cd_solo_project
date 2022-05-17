from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.book import Book
import re	
 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db = "solo_project"
    
    def __init__(self,data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.book= []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (firstName, lastName, email, password) VALUES(%(firstName)s, %(lastName)s, %(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_user_with_books(cls, data):
        query = "SELECT * FROM user LEFT JOIN book ON user.id = book.user_id WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        user = cls(results[0])
        for row in results:
            book_data = {
                'id': row['book.id'],
                'title': row['title'],
                'author': row['author'],
                'release_year': row['release_year'],
                'createdAt': row['book.createdAt'],
                'updatedAt': row['book.updatedAt']
            }
            user.book.append(Book(book_data))
        return user

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
    
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['firstName']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['lastName']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid