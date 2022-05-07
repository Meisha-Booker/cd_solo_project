from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  
from flask import flash

class Book:
    
    
    
    
    @staticmethod
    def validate_burger(burger):
        is_valid = True 
        if len(burger['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(burger['bun']) < 3:
            flash("Bun must be at least 3 characters.")
            is_valid = False
        if int(burger['calories']) < 200:
            flash("Calories must be 200 or greater.")
            is_valid = False
        if len(burger['meat']) < 3:
            flash("Bun must be at least 3 characters.")
            is_valid = False
        return is_valid