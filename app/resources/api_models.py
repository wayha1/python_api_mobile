from flask_restx import fields
from app.extensions import api

ALLOWED_GENDERS = ["male", "female"]

profile_model = api.model("Profile", {
    "id": fields.Integer,  # Corrected to fields.Integer if it's an integer
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
    "gender": fields.String(enum=ALLOWED_GENDERS),
    "role": fields.String
})

profile_input_model = api.model("ProfileInput", {
    "username": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "gender": fields.String(enum=ALLOWED_GENDERS, required=True),
    "role": fields.String(required=True)
})
