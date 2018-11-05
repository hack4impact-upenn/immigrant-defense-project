import datetime

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app.decorators import *

from .. import db
from ..models import Reminder
from ..sms import send
from .forms import ScheduleNewReminderForm, SendNewReminderForm

reminder = Blueprint('reminder', __name__)


@reminder.route('/', methods=['GET'])
@login_required
def dashboard():
    """Dashboard to view and add text and email reminders."""
    return render_template(
        'reminder/index.html', reminders=Reminder.query.all())

@reminder.route('/send', methods=['GET', 'POST'])
def send_new_reminder_form():
    """Create a new reminder and send it immediately."""
    form = SendNewReminderForm()
    if form.validate_on_submit():
        now = datetime.datetime.now()
        reminder = Reminder(
            title=form.title.data,
            content=form.content.data,
            date=now.date(),
            time=now.time(),
            sent=True
        )
        db.session.add(reminder)
        try:  # TODO: Add flashes
            db.session.commit()
            send(reminder)
            return redirect(url_for('reminder.dashboard'))
        except IntegrityError:
            db.session.rollback()
    return render_template('reminder/send_form.html', form=form)


@reminder.route('/schedule', methods=['GET', 'POST'])
def schedule_new_reminder_form():
    """Create a new reminder and schedule it for later."""
    form = ScheduleNewReminderForm()
    if form.validate_on_submit():
        hour, am_pm = form.time.data.split(' ', 1)
        hour = (int(hour) % 12) + (12 if am_pm.lower() == 'pm' else 0)
        reminder = Reminder(
            title=form.title.data,
            content=form.content.data,
            date=form.date.data,
            time=datetime.time(hour=hour))
        db.session.add(reminder)
        try:  # TODO: Add flashes
            db.session.commit()
            return redirect(url_for('reminder.dashboard'))
        except IntegrityError:
            db.session.rollback()
    return render_template('reminder/schedule_form.html', form=form)
