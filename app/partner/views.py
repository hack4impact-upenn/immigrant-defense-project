from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import partner_required

partner = Blueprint('partner', __name__)


@partner.route('/', methods=['GET', 'POST'])
@login_required
@partner_required
def index():
    """Partner dashboard page."""
    return render_template('partner/index.html')
