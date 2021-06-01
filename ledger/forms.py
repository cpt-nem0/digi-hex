from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField

class RegistrationForm(FlaskForm):
    business_name = StringField(label="Business Name")
    owner_name = StringField(label="Owner Name")
    owner_email = StringField(label="Owner Email")
    owner_phone = IntegerField(label="Owner Phone no")
    password = PasswordField(label="Password")
    confirm_password = PasswordField(label="Confirm Password")
    register = SubmitField(label='Register')

class LoginForm(FlaskForm):
    user_email = StringField(label="E-mail")
    user_password = PasswordField(label="Password")
    login = SubmitField(label='Login')

class AddClientsForm(FlaskForm):
    client_name = StringField(label="Client Name")
    client_email = StringField(label="Client E-mail")
    client_phone = StringField(label="Client Phone")
    add_client = SubmitField(label="Add Client")
