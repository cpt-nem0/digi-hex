from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from ledger.schema import businessSchema

class RegistrationForm(FlaskForm):
    def validate_business_name(self, business_name_to_check):
        bName = businessSchema.objects(__raw__={'b_name':business_name_to_check.data}).first()

        if bName:
            raise ValidationError('Business with the same name already exists.')

    def validate_owner_email(self, owner_email_to_check):
        bEmail = businessSchema.objects(__raw__={'b_email':owner_email_to_check.data}).first()
        
        if bEmail:
            raise ValidationError('Provided Email Id already exists.')
        
    def validate_owner_phone(self, owner_phone_to_check):
        bMobile = businessSchema.objects(__raw__={'b_mobile':owner_phone_to_check.data}).first()

        if bMobile:
            raise ValidationError('Provided mobile number already exists.')

    business_name = StringField(label="Business Name", validators=[Length(max=30), DataRequired()])
    owner_name = StringField(label="Owner Name", validators=[Length(max=30), DataRequired()])
    owner_email = StringField(label="Owner Email", validators=[Email(), DataRequired()])
    owner_phone = IntegerField(label="Owner Phone no", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo('password'), DataRequired()])
    register = SubmitField(label='Register')


class LoginForm(FlaskForm):
    user_email = StringField(label="E-mail", validators=[DataRequired()])
    user_password = PasswordField(label="Password", validators=[DataRequired()])
    login = SubmitField(label='Login')


class AddClientsForm(FlaskForm):
    client_name = StringField(label="Client Name")
    client_email = StringField(label="Client E-mail")
    client_phone = StringField(label="Client Phone")
    add_client = SubmitField(label="Add Client")
