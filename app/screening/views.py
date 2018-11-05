from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)

from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.decorators import *
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import ScreeningQuestion
from app.screening.forms import ScreeningQuestionForm

screening = Blueprint('screening', __name__)


@screening.route('/')
@login_required
def index():
    """Screening page."""
    screening_questions = ScreeningQuestion.query.all()
    return render_template(
        'screening/index.html', screening_questions=screening_questions)


@screening.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_screening_question():
    form = ScreeningQuestionForm()
    type = "Add New"
    if form.validate_on_submit():
        screening_question = ScreeningQuestion(question=form.question.data)
        db.session.add(screening_question)
        db.session.commit()
        flash('Screening question successfully created', 'form-success')
        return render_template(
            'screening/add_screening_question.html', form=form, type=type)
    return render_template(
        'screening/add_screening_question.html', form=form, type=type)


@screening.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_screening_question(id):
    """Edit a screening question's title and description."""
    screening_question = ScreeningQuestion.query.get(id)
    if screening_question is None:
        abort(404)
    old_question = screening_question.question
    form = ScreeningQuestionForm()
    type = "Edit"
    if form.validate_on_submit():
        screening_question.question = form.question.data
        try:
            db.session.commit()
            flash('Screening question successfully changed.', 'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('Error Occurred. Please try again.', 'form-error')
        return render_template('screening/add_screening_question.html', form=form, type=type)
    form.question.data = screening_question.question
    return render_template('screening/add_screening_question.html', form=form, type=type)


@screening.route('/<int:id>/delete')
@login_required
@admin_required
def delete_screening_question(id):
    """Deletes the screening question"""
    screening_question = ScreeningQuestion.query.get(id)
    if screening_question is None:
        abort(404)
    db.session.delete(screening_question)
    try:
        db.session.commit()
        flash('Successfully deleted screening question', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error occurred. Please try again.', 'form-error')
        return redirect(url_for('screening.index'))
    return redirect(url_for('screening.index'))
