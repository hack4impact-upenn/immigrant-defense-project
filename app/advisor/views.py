from flask import Blueprint, render_template, flash
from flask_login import current_user, login_required

from app.decorators import advisor_required
from app.advisor.forms import EditAdvisorInfoForm
from app.models import User
from .. import db

advisor = Blueprint('advisor', __name__)


@advisor.route('/', methods=['GET', 'POST'])
@login_required
@advisor_required
def index():
    """Advisor dashboard page."""
    return render_template('advisor/index.html')

@advisor.route('/edit', methods=['GET', 'POST'])
@login_required
@advisor_required
def edit_profile():
    """Advisor edit page."""
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        abort(404)
    form = EditAdvisorInfoForm()
    if form.validate_on_submit():
        user.location = form.location.data
        user.clemency_familiarity = form.clemency_familiarity.data
        user.law_experience = form.law_experience.data
        user.bio = form.bio.data
        user.languages = form.languages.data
        db.session.commit()
        flash(
            'Profile for advisor {} successfully updated.'.format(
                user.full_name()), 'form-success')
    form.location.data = user.location
    form.clemency_familiarity.data = user.clemency_familiarity
    form.law_experience.data = user.law_experience
    form.bio.data = user.bio
    form.languages.data = user.languages
    return render_template('advisor/edit.html', user=user, form=form)

@advisor.route('/profile', methods=['GET', 'POST'])
@login_required
@advisor_required
def view_profile():
    """Advisor profile page."""
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        abort(404)
    return render_template('advisor/profile.html', user=user)
