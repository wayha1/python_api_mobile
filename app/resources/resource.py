from flask_restx import Resource, Namespace, abort
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.resources.api_models import *
from app.models import *
from app.extensions import db

authorizations = {
    "jsonWebToken" : {
        "type": "apiKey",
        "in" : "header",
        "name": "Authorization"
    }
}
ns_auth = Namespace('auth')
ns_profile = Namespace('profile', authorizations=authorizations)

ns_profile.decorators = [jwt_required()]
# Register User (username and password)
@ns_auth.route('/register')
class Register(Resource): 
    @ns_profile.expect(login_model)
    @ns_profile.marshal_with(user_model)
    def post(self):
        user = User(username=ns_profile.payload['username'], password_hash=generate_password_hash(ns_profile.payload["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201
    
# Login Endpoint
@ns_auth.route('/login')
class Login(Resource):
    @ns_profile.expect(login_model)
    def post(self):
        user = User.query.filter_by(username=ns_profile.payload["username"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password_hash, ns_profile.payload["password"]):
            return {"error": "Incorrect Password"}, 401
        return {"access_token": create_access_token(user.username)}
    
# Input profile
@ns_profile.route("/profile")
class ProfileAPIList(Resource):
    @ns_profile.doc(security="jsonWebToken")
    @ns_profile.marshal_list_with(profile_model)
    def get(self):
        return Profile.query.all()

    @ns_profile.doc(security="jsonWebToken")
    @ns_profile.expect(profile_input_model)
    @ns_profile.marshal_with(profile_model)
    def post(self):
        data = ns_profile.payload
        profile = Profile(
            username=data["username"],
            email=data["email"],
            gender=data["gender"],  
            role=data["role"]
        )
        db.session.add(profile)
        db.session.commit()
        return profile, 201

# Update and delete search profile by id
@ns_profile.route('/profile/<int:id>') 
class ProfileAPI(Resource):
    @ns_profile.doc(security="jsonWebToken")
    @ns_profile.marshal_with(profile_model)
    def get(self, id):
        profile = Profile.query.get(id)
        if profile is None:
            return abort(404, message="Profile not found.")
        return profile
    
    @ns_profile.doc(security="jsonWebToken")
    @ns_profile.expect(profile_input_model)
    @ns_profile.marshal_with(profile_model)
    def put(self, id):
        data = ns_profile.payload

        # Validate 'gender' field
        valid_genders = ["male", "female"]
        if "gender" in data and data["gender"].lower() not in valid_genders:
            return abort(400, message="Invalid value for 'gender'. Allowed values are 'male' or 'female'.")
        profile = Profile.query.get(id)

        if profile is None:
            # If the profile does not exist, create a new one
            profile = Profile(
                username=data["username"],
                email=data["email"],
                gender=data["gender"],
                role=data["role"]
            )
            db.session.add(profile)
        else:
            # If the profile exists, update its fields
            profile.username = data.get("username", profile.username)
            profile.gender = data.get("gender", profile.gender)
            profile.role = data.get("role", profile.role)

        db.session.commit()
        return profile
    
    @ns_profile.doc(security="jsonWebToken")
    def delete(self, id):
        profile = Profile.query.get(id)
        if profile is None:
            return abort(404, message="Profile not found.")

        db.session.delete(profile)
        db.session.commit()
        return {}, 204


