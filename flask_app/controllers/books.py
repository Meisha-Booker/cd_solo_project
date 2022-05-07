from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.book import Book
from flask_app.models.user import User


@app.route('/create/book', methods=['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Book.validate_tree(request.form):
        return redirect('/new/book')
    data = {
        "title": request.form["title"],
        "author": request.form["author"],
        "release_year": request.form["release_year"],
        "user_id": session["user_id"]
    }
    Book.save(data)
    return redirect('/profile_page')