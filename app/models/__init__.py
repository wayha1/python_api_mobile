from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    profile = db.relationship('Profile', back_populates='user')

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(10))
    role = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='profile')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    books = db.relationship('Book', back_populates='category')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False, unique=True)
    price = db.Column(db.String(20), nullable=False, unique=True)
    publisher = db.Column(db.String(20), nullable=False, unique=True)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  
    # Define the many-to-one relationship with back_populates
    category = db.relationship('Category', back_populates='books')
