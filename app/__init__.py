from flask import Flask
import os
from .config import Config
from .extensions import api, db, jwt
from .resources import *
from .models import *

def create_app():
    app = Flask(__name__)
    url = os.getenv("DATABASE_URL")
    config = Config()
    app.config.from_object(config)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = '07920ca637344a93a3403f4d062272f7'
        
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    register_ns(api)
    
    # @jwt.user_identity
    # def user_identity_lookup(user): 
    #     return user.id if user and hasattr(user, 'id') else None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()
    
    return app
