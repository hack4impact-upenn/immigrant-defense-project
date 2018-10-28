from flask import (
    Blueprint,
    render_template,
)
from flask_login import login_required

advisor = Blueprint('advisor', __name__)


# TODO: add advisor_required decorator
@advisor.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Advisor dashboard page."""
    return render_template('advisor/index.html')
