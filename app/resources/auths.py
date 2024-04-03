from flask_jwt_extended import jwt_required, create_access_token,get_jwt,get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Resource, Namespace, abort
from app.resources.api_models import *
from app.models import *
from app.extensions import db

ns_auth = Namespace('auth')


# Register User (username and password)
@ns_auth.route('/register')
class Register(Resource): 
    @ns_auth.expect(register_model)
    @ns_auth.marshal_with(register_ouput_model)
    def post(self):
        data = ns_auth.payload
        
        if User.query.filter_by(username=data['username']).first() is not None:
            return {"message": "Username already exists"}, 409
        if User.query.filter_by(email=data['email']).first() is not None:
            return {"message": "Email already exists"}, 409
        
        user = User(username=data['username'],
                    email=data['email'],
                    password_hash=generate_password_hash(data['password']),
                    gender=data['gender'],
                    role='user')
        
        print(user)
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.username)

        # Create a corresponding profile
        # profile = Profile(username=data['username'],
        #             email=data['email'],
        #             password_hash=generate_password_hash(data['password']),
        #             gender=data['gender'],
        #             role='user')
        
        # profile.access_token = access_token
        
        # db.session.add(profile)
        # db.session.commit()

        return {"user":user,"access_token":access_token}, 201  
    
# Login Endpoint
@ns_auth.route('/login')
class Login(Resource):
    @ns_auth.expect(login_model)
    def post(self):

        user = User.query.filter_by(username=ns_auth.payload["username"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password_hash, ns_auth.payload["password"]):
            return {"error": "Incorrect Password"}, 401
        
         # Generate access token
        access_token = create_access_token(identity=user.username)
        
        # Save access token to user
        user.access_token = access_token
        db.session.commit()
        
        return {"access_token": access_token}
    
# Logout Endpoint
@ns_auth.route('/logout')
class Logout(Resource):
    @jwt_required()
    @ns_auth.doc(security="jsonWebToken")
    def post(self):
        jti = get_jwt()["jti"]  # Get the JWT ID (jti) of the current token
        token = TokenBlocklist(jti=jti)
        db.session.add(token)
        db.session.commit()
        return {"message": "Successfully logged out"}, 200

    
# Protected Endpoint
@ns_auth.route("/protected")
class Protected(Resource):
    @jwt_required()
    @ns_auth.doc(security="jsonWebToken")
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return {"error": "User not found"}, 404
        return {"user": user.username, "email": user.email, "role": user.role}
