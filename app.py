"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()

@app.route('/')
def redirect_users():
    return redirect("/users")

@app.route("/users")
def list_users():

    users=User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/<int:user_id>")
def show_detail(user_id):

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/create_user")
def create_new_user():
    
    return render_template("Create_user.html")

@app.route("/", methods=["POST"])
def add_user():
    """Add pet and redirect to list."""

    first_name = request.form['First']
    last_name = request.form['Last']
    image_url = request.form['Image']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    
    user = User.query.get_or_404(user_id)

    return render_template("/edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")
