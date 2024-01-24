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

category_model = api.model("CategoryModel", {
    "id": fields.Integer,
    "name": fields.String,
    # "books": fields.List(fields.Nested(api.model('BookModel', {
    #     'id': fields.Integer,
    #     'title': fields.String,
    #     'description': fields.String,
    # })))
})

category_input_model = api.model("CategoryInputModel", {
    "name": fields.String,
    # "books": fields.List(fields.Nested(api.model('BookModel', {
    #     'id': fields.Integer,
    #     'title': fields.String,
    #     'description': fields.String,
    # })))
})

book_model = api.model("BookModel", {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "price": fields.String,
    "publisher": fields.String,
    "category_id": fields.Integer
})

book_input_model = api.model("BookInput", {
    "title": fields.String(required=True),
    "description": fields.String(required=True),
    "price": fields.String,
    "publisher": fields.String,
    "category_id": fields.Integer(required=True)
})
