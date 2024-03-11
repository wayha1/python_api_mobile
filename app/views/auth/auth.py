from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, logout_user
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()  # Create an instance of LoginManager

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={'placeholder': 'username'})
    password = PasswordField('Password', widget=PasswordInput(hide_value=True), validators=[DataRequired()], render_kw={'placeholder': 'password'})
    remember = BooleanField('Remember me')
    submit_login = SubmitField('Login')

@auth_bp.route('/login')
def show_login():
    form = LoginForm()
    return render_template('login.html', form=form)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=remember)
        flash('Login successful', 'success')
        return redirect(url_for('main.profile'))
    else:
        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('auth.show_login'))  # Redirect to login page on unsuccessful login

@auth_bp.route('/signup')
def signup():
    form = LoginForm()
    return render_template('signup.html', form=form)

@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user:
        flash('Username already exists. Please choose a different one.', 'danger')
        return redirect(url_for('auth.signup'))
    
    new_user = User(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Account created successfully! You can now log in.', 'success')
    return redirect(url_for('auth.show_login'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.show_login'))
