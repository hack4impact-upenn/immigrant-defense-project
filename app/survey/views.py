from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import SurveyQuestion
from app.survey.forms import NewSurveyQuestion

survey = Blueprint('survey', __name__)

@survey.route('/')
def manage_questions():
    """View and manage survey questions."""
    survey_questions = SurveyQuestion.query.all()
    return render_template('survey/manage_questions.html', survey_questions=survey_questions)

@survey.route('/new', methods=['GET', 'POST'])
def new_question():
    form = NewSurveyQuestion()
    type = "Add New"
    if form.validate_on_submit():
        survey_question = SurveyQuestion(
            content=form.content.data,
            description = form.description.data)
        db.session.add(survey_question)
        db.session.commit()
        flash('Survey question successfully created', 'form-success')
        return render_template('survey/new_question.html', form=form, type=type)
    return render_template('survey/new_question.html', form=form, type=type)

@survey.route('/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    """Edit a survey question's title and description."""
    survey_question = SurveyQuestion.query.get(id)
    if survey_question is None:
        abort(404)
    form = NewSurveyQuestion()
    form.content.data = survey_question.content
    form.description.data = survey_question.description
    form_type = "Edit"

    if form.validate_on_submit():
        survey_question.content = form.content.data
        survey_question.description = form.description.data
        survey_question.type = form.type.data
        survey_question.screen = form.screen.data
        try:
            db.session.commit()
            flash('Survey question successfully edited.', 'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('An error has occurred. Please try again.', 'form-error')
        return render_template('survey/new_question.html', form=form, type=form_type)
    return render_template('survey/new_question.html', form=form, type=form_type)


@survey.route('/<int:id>/delete')
def delete_question(id):
    """Deletes the survey question"""
    survey_question = SurveyQuestion.query.get(id)
    if survey_question is None:
        abort(404)
    db.session.delete(survey_question)
    try:
        db.session.commit()
        flash('Successfully deleted survey question', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error occurred. Please try again.', 'form-error')
        return redirect(url_for('survey.manage_questions'))
    return redirect(url_for('survey.manage_questions'))
