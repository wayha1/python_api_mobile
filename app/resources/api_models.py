from flask_restx import fields
from app.extensions import api

login_model = api.model("LoginModel", {
    "username" : fields.String,
    "password" : fields.String
})

user_model = api.model("UserModel", {
    "id": fields.Integer,
    "username": fields.String
})

profile_model = api.model("Profile", {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "gender": fields.String, 
    "role": fields.String
})

profile_input_model = api.model("ProfileInput", {
    "username": fields.String(required=True),
    "email": fields.String(required=True),
    "gender": fields.String(required=True), 
    "role": fields.String(required=True)
})
