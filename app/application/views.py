from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.models import Application, User

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
    application = Application.query.join(User).filter(User.id == user_id).get(user_id)
    if application is None:
        abort(404)
    old_title = default_checklist_item.title
    form = DefaultChecklistItemForm()
    type = "Edit"
    if form.validate_on_submit():
        default_checklist_item.title = form.title.data
        default_checklist_item.description = form.description.data
        try:
            db.session.commit()
            flash(
                'Default checklist item {} successfully changed.'.format(
                    old_title), 'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('Error Occurred. Please try again.', 'form-error')
        return render_template(
            'checklist/edit_checklist_item.html', form=form, type=type)
    form.title.data = default_checklist_item.title
    form.description.data = default_checklist_item.description
    return render_template(
        'checklist/edit_checklist_item.html', form=form, type=type)