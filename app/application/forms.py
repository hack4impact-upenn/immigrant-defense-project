from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import HiddenField, SubmitField, SelectField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app import db
from app.models import Role, User


class AssignAdvisorForm(Form):
    advisor = SelectField('Advisor Name', choices=[])
    applicant_ids = HiddenField('Applicant Ids')
    submit = SubmitField('Assign Advisor')
    