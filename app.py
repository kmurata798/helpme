from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os

app = Flask(__name__)

client = MongoClient()
db = client.posts
posts = db.posts

@app.route('/')
def posts_index():
    """Show all posts."""
    return render_template('posts_index.html', posts=posts.find())

@app.route('/posts/new')
def posts_new():
    """Create a new post."""
    return render_template('posts_new.html')

@app.route('/posts', methods=['POST'])
def posts_submit():
    """Submit a new post."""
    post = {
        'title': request.form.get('title'),
        'description': request.form.get('description')
    }
    posts.insert_one(post)
    return redirect(url_for('posts_index'))

if __name__ == '__main__':
    app.run(debug=True)