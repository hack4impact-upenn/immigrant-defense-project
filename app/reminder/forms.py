import itertools
from flask_wtf import Form
from wtforms.fields import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField


class NewReminderForm(Form):
    title = StringField(
        'Reminder title',
        validators=[InputRequired(), Length(1, 64)]
    )
    content = TextAreaField(
        'Content',
        validators=[InputRequired()]
    )
    date = DateField(
        'Date',
        format='%Y-%m-%d',
        validators=[InputRequired()]
    )
    hours = ['12'] + [str(x) for x in range(1, 12)]
    time = SelectField(
        'Time',
        choices=[(f'{h} AM', f'{h} AM') for h in hours] +
                [(f'{h} PM', f'{h} PM') for h in hours],
        validators=[InputRequired()]
    )
    submit = SubmitField('Add Reminder')
