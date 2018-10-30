from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.models import Application, User

application = Blueprint('application', __name__)

@login_required
@application.route('/')
def index():
    print(current_user.role_id)
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
    application = Application.query.filter_by(user=current_user).first()
    if not application:
        return redirect(404)
    return render_template('application/profile.html', application=application)
