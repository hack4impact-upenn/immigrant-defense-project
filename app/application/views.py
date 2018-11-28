from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.models import Application, User, Stage
from app.application.forms import AssignAdvisorForm

application = Blueprint('application', __name__)


@login_required
@application.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_applicant():
        return redirect(url_for('application.view', user_id=current_user.id))
    elif current_user.is_screener():
        return redirect(404)
    elif current_user.is_admin():
        applicants = User.query.filter(User.application != None).all()
    elif current_user.is_advisor():
        applicants = User.query.filter(
            User.application != None and User.application.legal_adivsor == current_user).all()
    else:
        return redirect(404)

    advisor_form = AssignAdvisorForm()
    if advisor_form.validate_on_submit():
        for app_id in advisor_form.applicant_ids.data.split(','):
            user = User.query.filter_by(id=app_id).first()
            data = Application.query.filter_by(id=user.application_id).first()
            data.legal_advisor = advisor_form.advisor.data
            data.stage = Stage.MATCHED_ADVISOR if advisor_form.advisor.data is not None else Stage.UNMATCHED_PARTNER    
            db.session.add(data)
        db.session.commit()
        flash('Successfully assigned advisors!', 'form-success')
        return redirect(url_for('application.index'))

    return render_template(
        'application/dashboard.html',
        applicants=applicants,
        advisor_form=advisor_form)

# 
# @checklist.route('/user/<int:user_id>', methods=['GET'])
# def view(user_id):
#     """View all checklist items, specific to each user"""
#     """Finding user, then accessing application"""
#     user = User.query.get(user_id)
#     if user is None or user.application is None:
#         abort(404)
#     user_checklist_items = UserChecklistItem.query.filter_by(application_id=user.application.id)
#     return render_template(
#         'checklist/view_checklist_items.html',
#         user_checklist_items=user_checklist_items)


@login_required
@application.route('/<int:user_id>')
def view(user_id):
    if current_user.is_applicant() and current_user.id != user_id:
        return redirect(404)
    user = User.query.get(user_id)
    if not user.application:
        return redirect(404)
    return render_template('application/profile.html', user=user)
