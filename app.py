from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os

app = Flask(__name__)

client = MongoClient()
db = client.posts
posts = db.posts

@app.route('/')
def index():
    '''returns homepage'''
    return render_template('home.html', msg = 'I am good')

if __name__ == '__main__':
    app.run(debug=True)