from flask_restx import fields
from app.extensions import api

profile_model = api.model("Profile",{
    "id": fields.String,
    "username": fields.String,
    "email" : fields.String,
    "password" : fields.String,
    "gender" : fields.boolean
})

profile_input_model = api.model("ProfileInput",{
    "username": fields.String,
    "email" : fields.String,
    "password" : fields.String,
    "gender" : fields.boolean
})