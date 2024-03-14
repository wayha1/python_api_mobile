from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import api, db, jwt, login_manager
from .resources import *
from .models import *
from app.views.auth.auth import *
from app.views.main import *

def create_app():
    app = Flask(__name__)
    CORS(app)
    config = Config()
    
    app.config.from_object(config)
    app.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies"]
    app.config['SECRET_KEY'] = 'thisismysecretkeydontstealit'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = '07920ca637344a93a3403f4d062272f7'
    # app.config['UPLOAD_FOLDER'] = 'assets/'
   
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    register_ns(api)
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main)
    # app.register_blueprint(api_bp)
    
    # @jwt.user_identity
    # def user_identity_lookup(user): 
    #     return user.id if user and hasattr(user, 'id') else None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()

    return app
