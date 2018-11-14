from flask import (Blueprint, abort, flash, make_response, redirect, render_template, request,
                   url_for)
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import SurveyQuestion, SurveyOption, SurveyOptionAction, SurveyResponse
from app.survey.forms import generate_response_form, NewSurveyQuestion

survey = Blueprint('survey', __name__)


@survey.route('/', methods=['GET', 'POST'])
def index():
    question_id = request.cookies.get('question_id')
    if question_id:
        question = SurveyQuestion.query.get(question_id)
    else:
        question = SurveyQuestion.query.filter_by(rank=1).first()
        if not question:
            print('No questions')
            return redirect(404)
        question_id = question.id

    form = generate_response_form(question)
    if form.validate_on_submit():
        option_id = form.response.data
        option_ids = request.cookies.get('option_ids')
        if not option_ids:
            option_ids = str(option_id)
        else:
            option_ids += ',' + str(option_id)

        option = SurveyOption.query.get(option_id)
        next_question = SurveyQuestion.query.filter_by(rank=question.rank + 1).first()
        if option.next_action == SurveyOptionAction.CONTINUE and next_question:
            next_form = generate_response_form(next_question)
            resp = make_response(render_template('survey/survey.html', form=next_form))
            resp.set_cookie('question_id', str(next_question.id))
            resp.set_cookie('option_ids', option_ids)
            return resp
        elif option.next_action == SurveyOptionAction.STOP:
            # TODO: show error message (should be associated with the option as stop_description)
            # TODO: add a button that, when pressed, clears the cookies 'question_id' and 'option_ids'
            return f'STOP: {option.stop_description}'
        elif option.next_action == SurveyOptionAction.COMPLETED or next_question is None:
            # TODO: include user registration
            options = [SurveyOption.query.get(option_id) for option_id in option_ids]
            return render_template('survey/complete_survey.html', options=options)
        else: # option.next_action is a positive integer indicating the id of the next question
            next_question = SurveyQuestion.query.get(option.next_action)
            next_form = generate_response_form(next_question)
            resp = make_response(render_template('survey/survey.html', form=next_form))
            resp.set_cookie('question_id', str(next_question.id))
            resp.set_cookie('option_ids', option_ids)
            return resp

    resp = make_response(render_template('survey/survey.html', form=form))
    resp.set_cookie('question_id', str(question_id))
    return resp

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
