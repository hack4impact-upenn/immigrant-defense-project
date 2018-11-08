from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import HiddenField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .. import db
from app.models import Role, User


class AssignAdvisorForm(Form):
    advisor = QuerySelectField(
        'Advisor Name',
        allow_blank=True,
        validators=[InputRequired()],
        get_label='first_name',
        query_factory=lambda: db.session.query(User).filter(User.is_advisor(User)))
    applicant_ids = HiddenField('Applicant Ids')
    submit = SubmitField('Assign Advisor')
    