from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  
import re	
 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db = "solo_project"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
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

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
    
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","create")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","create")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","create")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","create")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","create")
        return is_valid