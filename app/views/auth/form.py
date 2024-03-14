from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={'placeholder': 'username'})
    email = StringField('Email', [DataRequired()], render_kw={'placeholder': 'email'})
    password = PasswordField('Password', widget=PasswordInput(hide_value=True), validators=[DataRequired()], render_kw={'placeholder': 'password'})
    gender = StringField('Gender', [DataRequired()], render_kw={'placeholder': 'gender'})
    remember = BooleanField('Remember me')
    submit_login = SubmitField('Login')
    
class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()], render_kw={'placeholder': 'Enter category'})
    submit = SubmitField('Submit')
