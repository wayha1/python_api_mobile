from app.extensions import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text())
    gender = db.Column(db.String(10))  # Adjust the length based on your needs
    role = db.Column(db.String)