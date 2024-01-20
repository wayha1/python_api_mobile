from flask_restx import Resource, Namespace, abort
from app.resources.api_models import profile_model, profile_input_model
from app.models import Profile
from app.extensions import db

ns_profile = Namespace('profile')

# input profile
@ns_profile.route("/profile")
class ProfileAPIList(Resource):
    @ns_profile.marshal_list_with(profile_model)
    def get(self):
        return Profile.query.all()

    @ns_profile.expect(profile_input_model)
    @ns_profile.marshal_with(profile_model, code=201)
    def post(self):
        data = ns_profile.payload  # Access payload data

        # Validate 'gender' field
        valid_genders = ["male", "female"]
        if "gender" in data and data["gender"].lower() not in valid_genders:
            return abort(400, message="Invalid value for 'gender'. Allowed values are 'male' or 'female'.")

        profile = Profile(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            gender=data["gender"],
            role=data["role"]
        )

        db.session.add(profile)
        db.session.commit()
        return profile, 201

# update and delete search profile
@ns_profile.route('/profile/<int:id>')  # Corrected route definition
class ProfileAPI(Resource):
    @ns_profile.marshal_with(profile_model)
    def get(self, id):
        profile = Profile.query.get(id)
        if profile is None:
            return abort(404, message="Profile not found.")
        return profile

    @ns_profile.expect(profile_input_model)
    @ns_profile.marshal_with(profile_model)
    def put(self, id):
        data = ns_profile.payload

        # Validate 'gender' field
        valid_genders = ["male", "female"]
        if "gender" in data and data["gender"].lower() not in valid_genders:
            return abort(400, message="Invalid value for 'gender'. Allowed values are 'male' or 'female'.")

        # Search for the profile by ID
        profile = Profile.query.get(id)

        if profile is None:
            # If the profile does not exist, create a new one
            profile = Profile(
                username=data["username"],
                email=data["email"],
                password=data["password"],
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
    
    def delete(self, id):
        profile = Profile.query.get(id)
        if profile is None:
            return abort(404, message="Profile not found.")

        db.session.delete(profile)
        db.session.commit()
        return {}, 204
