from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/helpme')
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()
posts = db.posts
# client = MongoClient(host=host)
# db = client.posts

@app.route('/')
def posts_index():
    """Show all posts."""
    return render_template('posts_index.html', posts=posts.find())

@app.route('/posts/new')
def posts_new():
    """Create a new post."""
    return render_template('posts_new.html', post={}, title='New Post')

@app.route('/posts', methods=['POST'])
def posts_submit():
    """Submit a new post."""
    post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos')
        # 'topic': request.form.get('topic')
    }
    # posts.insert_one(post)
    post_id = posts.insert_one(post).inserted_id
    print(post_id)
    return redirect(url_for('posts_show', post_id=post_id))

@app.route('/posts/<post_id>', methods=['GET'])
def posts_show(post_id):
    
    '''show specific post'''
    if request.method == 'GET':
        
        post = posts.find_one({'_id': ObjectId(post_id)})
        print(post)
        # return f'my ID is {post_id}'
        return render_template('posts_show.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
def posts_edit(post_id):
    '''shows the editing form for a post'''
    if request.method == 'GET':
        post = posts.find_one({'_id': ObjectId(post_id)})
        return render_template('posts_edit.html', post=post, title='Editing')
    if request.method == 'POST':
        post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos'),
        'topic': request.form.get('topic')
        }
        posts.update_one({'_id': ObjectId(post_id)}, {'$set': post})
        return redirect(url_for('posts_index'))
     
@app.route('/posts/<post_id>/delete', methods =['POST'])
def posts_delete(post_id):
    '''deletes a post'''
    posts.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('posts_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))