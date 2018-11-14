from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import SurveyQuestion, SurveyOption, SurveyOptionAction, SurveyResponse
from app.survey.forms import generate_response_form, NewSurveyQuestion

survey = Blueprint('survey', __name__)


@survey.route('/', methods=['GET', 'POST'])
def index():
    question = SurveyQuestion.query.filter_by(rank=1).first()
    if not question:
        return redirect(404)
    return redirect(url_for('survey.view_question', question_id=question.id))


@survey.route('/<int:question_id>', methods=['GET', 'POST'])
def view_question(question_id):
    question = SurveyQuestion.query.get(question_id)
    if not question:
        print(f'Invalid SurveyQuestion id: {question_id}')
        return redirect(404)
    form = generate_response_form(question)
    if form.validate_on_submit():
        option_id = form.response.data
        option = SurveyOption.query.get(option_id)
        if option.next_action == SurveyOptionAction.COMPLETED:
            return "COMPLETED"
        elif option.next_action == SurveyOptionAction.STOP:
            return "STOP"
        elif option.next_action == SurveyOptionAction.CONTINUE:
            question = SurveyQuestion.query.filter_by(rank=question.rank + 1).first()
            if not question:
                return "COMPLETED"
            return redirect(url_for('survey.view_question', question_id=question.id))
    return render_template('survey/question.html', form=form)


@survey.route('/manage')
def manage_questions():
    """View and manage survey questions."""
    survey_questions = SurveyQuestion.query.all()
    return render_template('survey/manage_questions.html', survey_questions=survey_questions)


@survey.route('/manage/new', methods=['GET', 'POST'])
def new_question():
    form = NewSurveyQuestion()
    type = "Add New"
    if form.validate_on_submit():
        survey_question = SurveyQuestion(
            content=form.content.data,
            description=form.description.data)
        db.session.add(survey_question)
        db.session.commit()
        flash('Survey question successfully created', 'form-success')
        return render_template('survey/new_question.html', form=form, type=type)
    return render_template('survey/new_question.html', form=form, type=type)


@survey.route('/manage/<int:id>', methods=['GET', 'POST'])
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


@survey.route('/manage/<int:id>/delete')
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
