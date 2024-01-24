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
ns_category = Namespace('category', description='Category operations')
ns_book = Namespace('book', description='Book operations')


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
        return Book.query.all()

    @ns_book.doc(security="jsonWebToken")
    @ns_book.expect(book_input_model)
    @ns_book.marshal_with(book_model)
    def post(self):
        data = ns_book.payload
        book = Book(
            title=data["title"],
            description=data["description"],
            price= data["price"],
            publisher= data['publisher'],
            category_id=data["category_id"]
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
        book = Book.query.get(id)
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
                price= data["price"],
                publisher= data['publisher'],
                category_id=data["category_id"]
            )
            db.session.add(book)
        else:
            # If the book exists, update its fields
            book.title = data.get("title", book.title)
            book.description = data.get("description", book.description)
            book.price = data.get("price", book.price)
            book.publisher = data.get("publisher", book.publisher)
            book.category_id = data.get("category_id", book.category_id)

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
