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
    return render_template('reminder/form.html', form=form)
