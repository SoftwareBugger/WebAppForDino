from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from os import environ
import os

UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'
app.config['UPLOADED_IMAGES_DEST'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('HEROKU_POSTGRESQL_TEAL_URL') or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)

# user loader
@login_manager.user_loader
def load_user(user_id):
    return reviewer.query.get(int(user_id))

class review(db.Model):
    id = db.Column(db.Integer, index = True, unique = True, primary_key = True)
    image = db.Column(db.String(300), index = True, unique = False)
    description = db.Column(db.String(2000), index = True, unique = False)
    rating = db.Column(db.Integer, index = True, unique = False)
    # Foreign key starts with a lowercase
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.id'))
    def __repr__(self):
        return "Review: {} Rating: {}".format(self.description, self.rating)

class reviewer(UserMixin, db.Model):
    id = db.Column(db.Integer, index = True, unique = True, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    # add the email and password_hash attributes here:
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), index=True, default = datetime.utcnow)
    isAdministrator = db.Column(db.Boolean())
    reviews = db.relationship('review', backref='reviewer', lazy = 'dynamic', cascade = "all, delete, delete-orphan")
    # String representation of the reviewer
    def __repr__(self):
        return "Reviewer: {} Email: {}".format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class item(db.Model):
    id = db.Column(db.Integer, index = True, unique = True, primary_key = True)
    name = db.Column(db.String(80), index = True, unique = True)
    reviews = db.relationship('review', backref = 'item', lazy = 'dynamic', cascade = "all, delete, delete-orphan")
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    icon = db.Column(db.String(300), index = True, unique = True)
    def __repr__(self):
        return "Name: {} Brand: {}".format(self.name, self.brand)

class brand(db.Model):
    id = db.Column(db.Integer, index = True, unique = True, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    image = db.Column(db.String(300), index = True, unique = True)
    description = db.Column(db.String(3000), index = True, unique = False)
    items = db.relationship('item', backref='brand', lazy = 'dynamic', cascade = "all, delete, delete-orphan")
    def __repr__(self):
        return "Name: {}".format(self.name)

db.create_all()
import routes
port = int(os.environ.get("PORT", 5001))
app.run(port=port, debug=True)