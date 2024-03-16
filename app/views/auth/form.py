from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField ,TextAreaField, FileField
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

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'Enter username'})
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': 'Enter email'})
    password = PasswordField('Password', widget=PasswordInput(hide_value=True), validators=[DataRequired()], render_kw={'placeholder': 'Enter password'})
    gender = StringField('Gender', validators=[DataRequired()], render_kw={'placeholder': 'Enter gender'})
    role = StringField('Role', validators=[DataRequired()], render_kw={'placeholder': 'Enter role'})
    profile_image = StringField('Profile_Image', validators=[DataRequired()], render_kw={'placeholder': 'Enter image'})

    submit = SubmitField('Submit')
    
class AuthorForm(FlaskForm):
    author_name = StringField('Author Name', validators=[DataRequired()], render_kw={'placeholder': 'Enter author name'})
    author_decs = TextAreaField('Author Description', validators=[DataRequired()], render_kw={'placeholder': 'Enter author description'})
    gender = StringField('Gender', validators=[DataRequired()], render_kw={'placeholder': 'Enter gender'})
    author_image = FileField('Author Image', validators=[DataRequired()])
    submit = SubmitField('Submit')