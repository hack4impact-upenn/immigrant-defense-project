from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from app import db

from app.screening.forms import (
    ScreeningQuestionForm
)
from app.models import ScreeningQuestion

screening = Blueprint('screening', __name__)

@screening.route('/')
def index():
    """Screening page."""
    return render_template('screening/index.html')

@screening.route('/add', methods=['GET', 'POST'])
def add_screening_question():
    form = ScreeningQuestionForm()
    if form.validate_on_submit():
        screening_question = ScreeningQuestion(
            question=form.question.data)
        db.session.add(screening_question)
        db.session.commit()
        flash('Screening question {} successfully created'.format(screening_question.question),
              'form-success')
        return render_template('screening/add_screening_question.html', form=form)
    return render_template('screening/add_screening_question.html', form=form)
