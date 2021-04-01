# Author: Alex Culp
# Description: form templates for login, passwords, etc.
# Last modified: 07-09-2016
# Notes: none
from wtforms import Form
from wtforms import StringField, TextField, PasswordField, SelectField, IntegerField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class Login(Form):
    username = StringField('username', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])

class AddCompanyForm(Form):
    # company id generated automatically
    name = StringField('Name', validators = [DataRequired()]) 
    street = StringField('Street Address', validators= [DataRequired()])
    city = StringField('City', validators= [DataRequired()])
    state = StringField('State', validators= [DataRequired()])
    zip_code = StringField('ZIP code', validators= [DataRequired()])
    image_url = StringField('Image URL', validators= [DataRequired()])
    bio = StringField('Company Bio (optional)', widget=TextArea())

class EditCompanyForm(Form):
    # company id generated automatically
    name = StringField('Name', validators = [DataRequired()]) 
    street = StringField('Street Address', validators= [DataRequired()])
    city = StringField('City', validators= [DataRequired()])
    state = StringField('State', validators= [DataRequired()])
    zip_code = StringField('ZIP code', validators= [DataRequired()])
    image_url = StringField('Image URL', validators= [DataRequired()])
    bio = StringField('Company Bio (optional)', widget=TextArea())


class AddCouponForm(Form):
    # coupon id generated automatically
    company_id = SelectField('Choose Company', validators=[DataRequired()])
    pts_required = IntegerField('Points Required', validators = [DataRequired()])
    summary = StringField('Coupon Summary', widget = TextArea(), validators = [DataRequired()])
    max_use = IntegerField('Max #', validators = [DataRequired()])

class EditCouponForm(Form):
    # coupon id generated automatically
    company_id = SelectField('Choose Company', validators=[DataRequired()])
    pts_required = IntegerField('Points Required', validators = [DataRequired()])
    summary = StringField('Coupon Summary', widget = TextArea(), validators = [DataRequired()])
    max_use = IntegerField('Max #', validators = [DataRequired()])

