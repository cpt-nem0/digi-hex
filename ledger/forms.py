from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import Length, EqualTo, Email, DataRequired, Regexp, ValidationError
from ledger.schema import Businesses
from flask import session

class RegistrationForm(FlaskForm):

    def validate_owner_email(self, owner_email_to_check):
        bEmail = Businesses.objects(__raw__={'b_email':owner_email_to_check.data}).first()
        
        if bEmail:
            raise ValidationError('Provided Email Id already exists.')
        
    def validate_owner_phone(self, owner_phone_to_check):
        bMobile = Businesses.objects(__raw__={'b_mobile':owner_phone_to_check.data}).first()

        if bMobile:
            raise ValidationError('Provided mobile number already exists.')

    business_name = StringField(label="Business Name", validators=[Length(max=30), DataRequired()])
    owner_name = StringField(label="Owner Name", validators=[Length(max=30), DataRequired()])
    owner_email = StringField(label="Owner Email", validators=[Email(), DataRequired()])
    owner_phone = StringField(label="Owner Phone no", validators=[Regexp('^[6-9]\d{9}$', message="Invalid Mobile Number"), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo('password'), DataRequired()])
    register = SubmitField(label='Register')


class LoginForm(FlaskForm):
    user_email = StringField(label="E-mail", validators=[DataRequired()])
    user_password = PasswordField(label="Password", validators=[DataRequired()])
    login = SubmitField(label='Login')


class AddClientsForm(FlaskForm):

    def validate_client_email(self, client_email_to_check):
        userData = Businesses.objects(b_id=session['user_id']).first()
        cEmail = [client.clientEmail for client in userData.clients]
        if client_email_to_check.data in cEmail:
            raise ValidationError('Client with same E-mail already exists')
    
    def validate_client_phone(self, client_phone_to_check):
        userData = Businesses.objects(b_id=session['user_id']).first()
        cMobile = [client.clientMobile for client in userData.clients]
        if int(client_phone_to_check.data) in cMobile:
            raise ValidationError('Client with same Mobile no. already exists')


    client_name = StringField(label="Client Name", validators=[Length(max=30), DataRequired()])
    client_email = StringField(label="Client E-mail", validators=[Email(), DataRequired()])
    client_phone = StringField(label="Client Phone", validators=[Regexp('^[6-9]\d{9}$', message="Invalid Mobile Number"), DataRequired()])
    add_client = SubmitField(label="Add Client")


class paymentRequest(FlaskForm):
    accept = SubmitField(label="Accept Payment")
    decline = SubmitField(label="Decline Payment")


class paymentForm(FlaskForm):
    emails = SelectField(label='Select Client', choices=[])
    amount = IntegerField(label='Amount')
    remarks = StringField(label='Remarks')
    sent = SubmitField(label='Request Payment via Email')