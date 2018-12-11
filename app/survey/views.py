from flask import (Blueprint, abort, flash, make_response, redirect, render_template, request,
                   url_for)
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import SurveyQuestion, SurveyOption, SurveyOptionAction, SurveyResponse
from app.survey.forms import generate_response_form, NewSurveyQuestion

survey = Blueprint('survey', __name__)


@survey.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated and not current_user.is_admin():
        return redirect(404)

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
            return render_template('survey/stop_survey.html', stop_message=option.stop_description)
        elif option.next_action == SurveyOptionAction.COMPLETED or next_question is None:
            option_ids = option_ids.split(',')
            options = [SurveyOption.query.get(option_id) for option_id in option_ids]
            return render_template('survey/complete_survey.html', options=options)
        else:  # option.next_action is a positive integer indicating the id of the next question
            next_question = SurveyQuestion.query.get(option.next_action)
            next_form = generate_response_form(next_question)
            resp = make_response(render_template('survey/survey.html', form=next_form))
            resp.set_cookie('question_id', str(next_question.id))
            resp.set_cookie('option_ids', option_ids)
            return resp

    resp = make_response(render_template('survey/survey.html', form=form))
    resp.set_cookie('question_id', str(question_id))
    return resp


@survey.route('/clear')
def restart_survey():
    resp = make_response(redirect(url_for('survey.index')))
    # clear cookies
    resp.set_cookie('question_id', '', expires=0)
    resp.set_cookie('option_ids', '', expires=0)
    return resp


@survey.route('/manage')
def manage_questions():
    """View and manage survey questions."""
    questions = SurveyQuestion.query.all()
    return render_template('survey/manage.html', questions=questions)


@survey.route('/manage/new', methods=['GET', 'POST'])
def new_question():
    form = NewSurveyQuestion()
    type = "Add New"
    questions = SurveyQuestion.query.all()
    if form.validate_on_submit():
        survey_question = SurveyQuestion(
            content=form.content.data,
            description=form.description.data,
            rank=SurveyQuestion.next_rank())
        db.session.add(survey_question)
        db.session.commit()
        flash('Survey question successfully created', 'form-success')
        return redirect(url_for('survey.manage_questions'))

    return render_template('survey/new_question.html', form=form, type=type, questions=questions, options=[])


@survey.route('/manage/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    """Edit a survey question's title and description."""
    survey_question = SurveyQuestion.query.get(question_id)
    if survey_question is None:
        return redirect(404)

    form = NewSurveyQuestion()
    form_type = 'Edit'
    questions = SurveyQuestion.query.all()

    def parse_options(options_str):
        delimiter = '!@#$%'
        # string should be in the form of:
        # id [delimiter] content [delimiter] next_action [delimiter] stop_description[
        option_list = options_str.split(delimiter)
        print(option_list)
        print(len(option_list))
        if len(option_list) < 4:
            return
        existing_option_ids = set([o.id for o in survey_question.options])
        print(question_id)
        for i in range(0, len(option_list) - 1, 4):
            # Parse the options
            option_id = option_list[i]
            option_content = option_list[i + 1]
            option_next_action = option_list[i + 2]
            option_stop_description = option_list[i + 3]
            if option_id in existing_option_ids:
                option = SurveyOption.query.get(option_id)
                option.content = option_content
                option.next_action = option_next_action
                option.stop_description = option_stop_description
            else:
                option = SurveyOption(
                    question_id=question_id,
                    content=option_content,
                    next_action=option_next_action,
                    stop_description=option_stop_description)
            db.session.add(option)
        for option_id in existing_option_ids:
            db.session.delete(SurveyOption.query.get(option_id))

    if form.validate_on_submit():
        survey_question.content = form.content.data
        survey_question.description = form.description.data
        try:
            parse_options(form.options.data)
            db.session.commit()
            flash('Survey question successfully edited.', 'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('An error has occurred. Please try again.', 'form-error')
        return redirect(url_for('survey.manage_questions'))

    form.content.data = survey_question.content
    form.description.data = survey_question.description
    return render_template('survey/new_question.html', form=form, type=form_type, questions=questions, options=survey_question.options)


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
