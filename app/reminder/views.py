import datetime
import pytz

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .forms import NewReminderForm
from .. import db
from ..models import Reminder

reminder = Blueprint('reminder', __name__)


@reminder.route('/', methods=['GET'])
def dashboard():
    """Dashboard to view and add text and email reminders."""
    return render_template('reminder/index.html')


@reminder.route('/new', methods=['GET', 'POST'])
def new_form():
    """Create a new reminder."""
    form = NewReminderForm()
    if form.validate_on_submit():
        hour, am_pm = form.time.data.split(' ', 1)
        hour = (int(hour) % 12) + (12 if am_pm.lower() == 'pm' else 0)
        reminder = Reminder(
            title=form.title.data,
            content=form.content.data,
            date=form.date.data,
            time=datetime.time(hour=hour)
        )
        db.session.add(reminder)
        try:  # TODO: Add flashes
            db.session.commit()
            return redirect(url_for('reminder.dashboard'))
        except:
            db.session.rollback()
    return render_template('reminder/form.html', form=form)
