from flask_restx import fields
from app.extensions import *

login_model = api.model("LoginModel", {
    "username": fields.String,
    "password": fields.String
})
register_model = api.model("RegisterModel",{
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
    "gender": fields.String,
    "role": fields.String,
})

user_model = api.model("UserModel", {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "password_hash": fields.String,
    "gender": fields.String,
    "role": fields.String,
})

profile_model = api.model("ProfileModel", {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "password_hash": fields.String,
    "gender": fields.String,
    "role": fields.String,
    "profile_image": fields.String(attribute=lambda x: x.profile_image)
})

profile_input_model = api.model("ProfileInputModel", {
    "username": fields.String(required=True),
    "email": fields.String(required=True),
    "password_hash": fields.String,
    "gender": fields.String(required=True),
    "role": fields.String(required=True),
    "profile_image": fields.String
})

author_model = api.model("AuthorModel", {
    "id": fields.Integer,
    "author_name": fields.String,
    "author_decs": fields.String,
    "gender": fields.String,
    "author_image": fields.String(attribute=lambda x: x.author_image)
})

author_input_model = api.model("AuthorInputModel", {
    "author_name": fields.String,
    "author_decs": fields.String,
    "gender": fields.String,
    "author_image": fields.String
})

category_model = api.model("CategoryModel", {
    "id": fields.Integer,
    "name": fields.String,
})

category_input_model = api.model("CategoryInputModel", {
    "name": fields.String,
})

book_model = api.model("BookModel", {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "price": fields.String,
    "publisher": fields.String,
    "category_id": fields.Integer,
    "author_id": fields.Integer,
    "book_image": fields.String,
    "book_pdf": fields.String
})

book_input_model = api.model("BookInputModel", {
    "title": fields.String(required=True),
    "description": fields.String(required=True),
    "price": fields.String,
    "publisher": fields.String,
    "category_id": fields.Integer(required=True),
    "author_id": fields.Integer(required=True),
    "book_image": fields.String,
    "book_pdf": fields.String
})

payment_model = api.model("PaymentModel", {
    "id" : fields.Integer,
    "user_id" : fields.Integer,
    "book_id" : fields.Integer,
    "price" : fields.Float
})
payment_input_model = api.model("PaymentInputModel", {
    "user_id" : fields.Integer,
    "book_id" : fields.Integer,
    "price" : fields.Float
})

# image_model = api.model("ImageModel", {
#     "id": fields.Integer,
#     "file_path": fields.String
# })

# image_input_model = api.model("ImageInputModel", {
#     "file_path": fields.String(required=True)
# })

# pdf_model = api.model("PDFModel", {
#     "id": fields.Integer,
#     "file_path": fields.String
# })

# pdf_input_model = api.model("PDFInputModel", {
#     "file_path": fields.String(required=True)
# })
