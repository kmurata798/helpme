from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os

app = Flask(__name__)

client = MongoClient()
db = client.posts
posts = db.posts

# @app.route('/')
# def index():
#     '''returns homepage'''
#     return render_template('home.html', msg = 'I am good')

posts = [
    { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
    { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
]

@app.route('/')
def posts_index():
    """Show all posts."""
    return render_template('posts_index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)