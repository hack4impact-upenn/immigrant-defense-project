from flask import Blueprint, render_template, flash
from flask_login import current_user, login_required

from app.decorators import screener_required
from app.models import User
from app.screener.forms import EditScreenerInfoForm
from .. import db

screener = Blueprint('screener', __name__)


@screener.route('/', methods=['GET', 'POST'])
@login_required
@screener_required
def index():
    """Screener dashboard page."""
    return render_template('screener/index.html')

@screener.route('/edit', methods=['GET', 'POST'])
@login_required
@screener_required
def edit_profile():
    """Screener edit page."""
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        abort(404)
    form = EditScreenerInfoForm()
    if form.validate_on_submit():
        user.location = form.location.data
        user.immigrant_experience = form.immigrant_experience.data
        user.crime_experience = form.crime_experience.data
        user.bio = form.bio.data
        user.languages = form.languages.data
        db.session.commit()
        flash(
            'Profile for screener {} successfully updated.'.format(
                user.full_name()), 'form-success')
    form.location.data = user.location
    form.immigrant_experience.data = user.immigrant_experience
    form.crime_experience.data = user.crime_experience
    form.bio.data = user.bio
    form.languages.data = user.languages
    return render_template('screener/edit.html', user=user, form=form)
