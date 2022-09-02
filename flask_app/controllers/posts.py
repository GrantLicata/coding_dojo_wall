from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import post
from flask_app.models import user
from flask_app.controllers import users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/post/create', methods=['POST'])
def create_post():
    data = {
        "content": request.form['content'],
        "user_id": session['user_id']
    }
    print("About to save data!")
    if not post.Post.validate_post(data):
        return redirect('/dojo_wall')
    post.Post.save(data)
    return redirect('/dojo_wall')

@app.route('/post/delete', methods=['POST'])
def delete_post():
    data = {
        "id": request.form['post_id']
    }
    post.Post.delete(data)
    return redirect('/dojo_wall')

