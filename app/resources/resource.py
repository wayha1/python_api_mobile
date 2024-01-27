from flask_restx import Resource, Namespace, abort
from flask import request,send_from_directory
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import current_app
from cloudinary.uploader import upload
import os
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
ns = Namespace('img')
ns_profile = Namespace('profile', authorizations=authorizations)
ns_author = Namespace('author', authorizations=authorizations)
ns_category = Namespace('category', description='Category operations', authorizations=authorizations)
ns_book = Namespace('book', description='Book operations', authorizations=authorizations)


ns_profile.decorators = [jwt_required()]
ns_author.decorators = [jwt_required()]
ns_category.decorators = [jwt_required()]
ns_book.decorators = [jwt_required()]

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

@ns_category.route("/category")
class CategoryAPIList(Resource):
    @ns_category.doc(security="jsonWebToken")
    @ns_category.marshal_list_with(category_model)
    def get(self):
        return Category.query.all()

    @ns_category.doc(security="jsonWebToken")
    @ns_category.expect(category_input_model)
    @ns_category.marshal_with(category_model)
    def post(self):
        data = ns_category.payload
        category = Category(name=data["name"])
        db.session.add(category)
        db.session.commit()
        return category, 201

# Update and delete category by id
@ns_category.route('/category/<int:id>') 
class CategoryAPI(Resource):
    @ns_category.doc(security="jsonWebToken")
    @ns_category.marshal_with(category_model)
    def get(self, id):
        category = Category.query.get(id)
        if category is None:
            return abort(404, message="Category not found.")
        return category
    
    @ns_category.doc(security="jsonWebToken")
    @ns_category.expect(category_input_model)
    @ns_category.marshal_with(category_model)
    def put(self, id):
        data = ns_category.payload
        category = Category.query.get(id)

        if category is None:
            # If the category does not exist, create a new one
            category = Category(name=data["name"])
            db.session.add(category)
        else:
            # If the category exists, update its fields
            category.name = data.get("name", category.name)

        db.session.commit()
        return category
    
    @ns_category.doc(security="jsonWebToken")
    def delete(self, id):
        category = Category.query.get(id)
        if category is None:
            return abort(404, message="Category not found.")

        db.session.delete(category)
        db.session.commit()
        return {}, 204

# Book Resource
@ns_book.route("/book")
class BookAPIList(Resource):
    @ns_book.doc(security="jsonWebToken")
    @ns_book.marshal_list_with(book_model)
    def get(self):
        # Include the 'author' relationship in the query to fetch author information
        return Book.query.options(db.joinedload(Book.author)).all()

    @ns_book.doc(security="jsonWebToken")
    @ns_book.expect(book_input_model)
    @ns_book.marshal_with(book_model)
    def post(self):
        data = ns_book.payload

        # Check if the provided author_id exists
        author = Author.query.get(data["author_id"])
        if author is None:
            return abort(400, message="Author not found.")

        # Create a new book with the specified author and category
        book = Book(
            title=data["title"],
            description=data["description"],
            price=data["price"],
            publisher=data['publisher'],
            category_id=data["category_id"],
            author_id=data["author_id"]
        )
        db.session.add(book)
        db.session.commit()
        return book, 201

# Update and delete book by id
@ns_book.route('/book/<int:id>') 
class BookAPI(Resource):
    @ns_book.doc(security="jsonWebToken")
    @ns_book.marshal_with(book_model)
    def get(self, id):
        # Include the 'author' relationship in the query to fetch author information
        book = Book.query.options(db.joinedload('author')).get(id)
        if book is None:
            return abort(404, message="Book not found.")
        return book

    @ns_book.doc(security="jsonWebToken")
    @ns_book.expect(book_input_model)
    @ns_book.marshal_with(book_model)
    def put(self, id):
        data = ns_book.payload
        book = Book.query.get(id)

        if book is None:
            # If the book does not exist, create a new one
            book = Book(
                title=data["title"],
                description=data["description"],
                price=data["price"],
                publisher=data['publisher'],
                category_id=data["category_id"],
                author_id=data["author_id"]
            )
            db.session.add(book)
        else:
            # If the book exists, update its fields
            book.title = data.get("title", book.title)
            book.description = data.get("description", book.description)
            book.price = data.get("price", book.price)
            book.publisher = data.get("publisher", book.publisher)
            book.category_id = data.get("category_id", book.category_id)
            book.author_id = data.get("author_id", book.author_id)

        db.session.commit()
        return book
    
    @ns_book.doc(security="jsonWebToken")
    def delete(self, id):
        book = Book.query.get(id)
        if book is None:
            return abort(404, message="Book not found.")

        db.session.delete(book)
        db.session.commit()
        return {}, 204

@ns_author.route('/author')
class AuthorAPIList(Resource):
    @ns_author.doc(security="jsonWebToken")
    @ns_author.marshal_list_with(author_model)
    def get(self):
        return Author.query.all()
    
    # Add the necessary decorators, expect, and marshal_with for creating an author
    @ns_author.doc(security="jsonWebToken")
    @ns_author.expect(author_input_model)
    @ns_author.marshal_with(author_model)
    def post(self):
        data = ns_author.payload
        author = Author(
            author_name=data["author_name"],
            author_decs=data["author_decs"],
            gender=data["gender"]
        )
        db.session.add(author)
        db.session.commit()
        return author, 201

# Define update and delete author by ID endpoint
@ns_author.route('/author/<int:id>')
class AuthorAPI(Resource):
    @ns_author.doc(security="jsonWebToken")
    @ns_author.marshal_with(author_model)
    def get(self, id):
        author = Author.query.get(id)
        if author is None:
            return abort(404, message="Author not found.")
        return author

    @ns_author.doc(security="jsonWebToken")
    @ns_author.expect(author_input_model)
    @ns_author.marshal_with(author_model)
    def put(self, id):
        data = ns_author.payload
        author = Author.query.get(id)

        if author is None:
            # If the author does not exist, create a new one
            author = Author(
                author_name=data["author_name"],
                author_decs=data["author_decs"],
                gender=data["gender"]
            )
            db.session.add(author)
        else:
            # If the author exists, update its fields
            author.author_name = data.get("author_name", author.author_name)
            author.author_decs = data.get("author_decs", author.author_decs)
            author.gender = data.get("gender", author.gender)

        db.session.commit()
        return author

    @ns_author.doc(security="jsonWebToken")
    def delete(self, id):
        author = Author.query.get(id)
        if author is None:
            return abort(404, message="Author not found.")

        db.session.delete(author)
        db.session.commit()
        return {}, 204
    

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt','png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
from flask import current_app, send_from_directory
from flask_restx import Resource, Api, Namespace, reqparse
from flask import request, abort
from werkzeug.utils import secure_filename
from models import db, ImageModel, Book
import cloudinary
from cloudinary.uploader import upload

cloudinary.config(
    cloud_name="dwt710mdu",
    api_key="946233553338359",
    api_secret="e9E1rxvU3WfxwOjJsARP7ZrutuE"
)

ns = Namespace('img', description='Image operations')

# Define your parser for image input
image_input_model = ns.model('ImageInput', {
    'file': fields.File(required=True, description='Image file', location='form')
})

# Define your model for image response
image_model = ns.model('Image', {
    'id': fields.Integer(readonly=True, description='Image ID'),
    'file_path': fields.String(required=True, description='Cloudinary URL of the image'),
    'created_at': fields.DateTime(description='Image upload timestamp')
})

@ns.route('/image')
class Image(Resource):
    @ns.expect(image_input_model)
    @ns.marshal_with(image_model)
    def post(self):
        try:
            file = request.files['file']

            if 'file' not in request.files:
                return abort(400, message="No file part")
            if file.filename == '':
                return abort(400, message="No selected file")

            if file and allowed_file(file.filename):
                # Upload the image to Cloudinary
                cloudinary_response = upload(file)

                # Get the Cloudinary URL of the uploaded image
                cloudinary_url = cloudinary_response['secure_url']

                # Create an ImageModel instance with the Cloudinary URL
                image = ImageModel(file_path=cloudinary_url)
                db.session.add(image)
                db.session.commit()

                # Associate the image with a specific book using the provided book_id
                data = ns.payload
                book_id = data.get('book_id')
                if book_id:
                    book = Book.query.get(book_id)
                    if book:
                        book.image = image
                        db.session.commit()

                return {"message": "File uploaded successfully", "file_path": cloudinary_url}, 201

            return abort(400, message="Invalid file extension")
        except Exception as e:
            return abort(500, message="Error uploading the file: {}".format(str(e)))

    @ns.marshal_with(image_model)
    def get(self):
        images = ImageModel.query.all()
        return images


@ns.route('/sample/<filename>')
class ServeStatic(Resource):
    def get(self, filename):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


# @ns.route('/image/<filename>')
# class ImageDetail(Resource):
#     @ns.marshal_with(image_model)
#     def get(self, filename):
#         images = ImageModel.query.filter_by(file_path=filename).all()
#         return images

#     @ns.expect(image_input_model)
#     @ns.marshal_with(image_model)
#     def post(self, filename):
#         # ... (your existing code)

#         @ns.marshal_with(image_model)
#         def delete(self, filename):
#             images = ImageModel.query.filter_by(file_path=filename).all()
#             for image in images:
#                 db.session.delete(image)
#             db.session.commit()
#             return {}, 204

# # Add a route to serve static files
# @ns.route('/static/<filename>')
# class ServeStatic(Resource):
#     def get(self, filename):
#         return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
