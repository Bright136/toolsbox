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


class Tool(db.Model):
    __tablename__ = 'tools'
    tool_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    website_url = db.Column(db.String(255), nullable=True)
    pricing = db.Column(db.String(50), nullable=True)
    avg_rating = db.Column(db.Float, nullable=True)
    categories = db.relationship('Category', secondary='tool_category', back_populates='tools')
    reviews = db.relationship('Review', back_populates='tool')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tools = db.relationship('Tool', secondary='tool_category', back_populates='categories')


class User():
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    access = db.Column(db.String, nullable=False)

class ToolCategory(db.Model):
    __tablename__ = 'tool_category'
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.tool_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)

# class Review(db.Model):
#     __tablename__ = 'reviews'
#     review_id = db.Column(db.Integer, primary_key=True)
#     tool_id = db.Column(db.Integer, db.ForeignKey('tools.tool_id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     comment = db.Column(db.Text, nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     tool = db.relationship('Tool', back_populates='reviews')




with app.app_context():
    db.create_all()


@app.route('/home')
def home():
    return 'Welcome Home'



if __name__ == '__main__':
    app.run(debug=True)