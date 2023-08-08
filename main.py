from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config['SECRET KEY'] = "5904a019aa274b4e9653b11601728270"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nocode.db"
# initialize the app with the extension
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, )
# db.init_app(app)


# Tool class represents tools in the database
class Tool(db.Model):
    """Class representing tools in the database."""

    __tablename__ = 'tools'
    tool_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    website_url = db.Column(db.String(255), nullable=True)
    pricing = db.Column(db.String(50), nullable=True)
    avg_rating = db.Column(db.Float, nullable=True)
    # Establish a many-to-many relationship with Category using ToolCategory table
    categories = db.relationship('Category', secondary='tool_category', back_populates='tools')
    # Establish a one-to-many relationship with Review
    reviews = db.relationship('Review', back_populates='tool')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Category class represents categories in the database
class Category(db.Model):
    """Class representing categories in the database."""

    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Establish a many-to-many relationship with Tool using ToolCategory table
    tools = db.relationship('Tool', secondary='tool_category', back_populates='categories')

# User class represents users in the database
class User(db.Model):
    """Class representing users in the database."""

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    access = db.Column(db.String, nullable=False)

# ToolCategory class represents the association table for Tool and Category
class ToolCategory(db.Model):
    """Class representing the association between Tool and Category."""

    __tablename__ = 'tool_category'
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.tool_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)

# Review class represents reviews in the database
class Review(db.Model):
    """Class representing reviews in the database."""

    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.tool_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Establish a many-to-one relationship with Tool
    tool = db.relationship('Tool', back_populates='reviews')





with app.app_context():
    db.create_all()


@app.route('/home')
def home():
    return 'Welcome Home'



if __name__ == '__main__':
    app.run(debug=True)