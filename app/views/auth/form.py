from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={
                            'placeholder' : 'Username'
    })
    password = PasswordField('Password', validators=[
        DataRequired()], render_kw={'placeholder': 'Password'})
    submit_login = SubmitField('Login')
