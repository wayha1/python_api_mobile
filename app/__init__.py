from flask import Flask, jsonify
from .extensions import api, db, jwt
from app.config import Config

def create_app():
    app = Flask(__name__)
    
    config = Config()
    app.config.from_object(config)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    return app