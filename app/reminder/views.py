import datetime

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
from flask_login import login_required
from app.decorators import *

reminder = Blueprint('reminder', __name__)


@reminder.route('/', methods=['GET'])
@login_required
def dashboard():
    """Dashboard to view and add text and email reminders."""
    return render_template('reminder/index.html', reminders=Reminder.query.all())


@reminder.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
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
