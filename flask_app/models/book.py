from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
class Book:
    db_name = 'solo_project'
    
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.author = db_data['author']
        self.release_year = db_data['release_year']
        self.created_at = db_data['createdAt']
        self.updated_at = db_data['updatedAt']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO book (title, author, release_year, user_id, createdAt, updatedAt) VALUES (%(title)s, %(author)s, %(release_year)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM book;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_books = []
        for row in results:
            print(row['title'])
            all_books.append(cls(row))
        return all_books

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM book WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE book SET title=%(title)s, author=%(author)s, release_year=%(release_year)s, updatedAt=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM book WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_book(book):
        is_valid = True
        if len(book['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters","book")
        if len(book['author']) < 2:
            is_valid = False
            flash("Author must be at least 2 characters","book")
        if book['release_year'] == "":
            is_valid = False
            flash("Please enter a release year","book")
        return is_valid