from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("login.html")
            

@app.route('/register', methods=["POST"])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    passwords = {
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : pw_hash
    }
    print(data['email'])
    # Post validation (will cause redirect if False)
    if not User.validate_user(data):
        return redirect('/')
    if not User.validate_password(passwords):
        return redirect('/')
    id = User.save(data)
    session['user_id'] = id
    print("This is the session after a registration:", session['user_id'])
    return redirect('/dojo_wall')


@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" :request.form["email"] 
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dojo_wall")

@app.route('/clear')
def clear_session():
    session.clear()
    print(session)
    return redirect('/')

@app.route('/dojo_wall')
def dojo_wall():
    if session == {}:
        return redirect('/')
    user_posts = Post.get_all_posts_with_creator()
    return render_template("dojo_wall.html", posts = user_posts)