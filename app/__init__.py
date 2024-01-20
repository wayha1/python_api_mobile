from flask import Flask, jsonify, request, make_response, render_template, session
from .extensions import api, db, jwt
from app.config import Config
from .resources.resource import *

def create_app():
    app = Flask(__name__)
    
    config = Config()
    app.config.from_object(config)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_Key'] ='07920ca637344a93a3403f4d062272f7'
        
    api.init_app(app)
    db.init_app(app)
    api.add_namespace(ns_profile)
    
        

    # jwt.init_app(app)
    
    # @app.route('/')
    # def home():
    #     if not session.get('logged_in'):
    #         return render_template('login.html')
    #     else:
    #         return "Logged in currently! "
    
    return app