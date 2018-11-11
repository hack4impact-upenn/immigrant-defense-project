from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.models import Application, User, Stage

application = Blueprint('application', __name__)


@login_required
@application.route('/')
def index():
    if current_user.is_applicant():
        return redirect(url_for('application.view'), current_user.id)
    elif current_user.is_screener():
        return redirect(404)
    elif current_user.is_admin():
        applicants = User.query.filter(User.application != None).all()
    elif current_user.is_advisor():
        applicants = []
        # applications = Application.query.filter_by(legal_advisor=current_user.id).all()
    return render_template('application/dashboard.html', applicants=applicants)


@login_required
@application.route('/<int:user_id>')
def view(user_id):
    if current_user.is_applicant() and current_user.id != user_id:
        return redirect(404)
    user = User.query.get(user_id)
    if not user.application:
        return redirect(404)
    return render_template('application/profile.html', application=user.application)

@login_required
@application.route('<int:user_id>/change_status_to_complete')
def change_status_to_complete(user_id):
    application = Application.query.join(User, User.application_id == Application.id).filter(User.id == user_id).first()
    if application is None:
        abort(404)

    checklist_complete = True

    for c in application.user_checklist_items:
        if c.documents == None:
            checklist_complete = False

    if checklist_complete:
        try:
            application.stage = Stage.COMPLETED_CHECKLIST
            db.session.commit()
            flash(
                'Application stage {} successfully changed to completed checklist.'.format(
                    application.user), 'application-stage-update-success')
        except Exception as e:
            db.session.rollback()
            flash('Error Occurred. Please try again.', 'application-stage-update-error')
    else:
        flash('Checklist not complete. Some documents were not uploaded.', 'application-stage-update-error')

    user = User.query.join(Application, User.application_id == Application.id).filter(User.application_id != None).all()
    return render_template(
        'application/dashboard.html', user=user)