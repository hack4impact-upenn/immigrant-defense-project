from flask import (
    Blueprint,
    render_template,
)
from flask_login import login_required
from app.decorators import advisor_required

advisor = Blueprint('advisor', __name__)


@advisor.route('/', methods=['GET', 'POST'])
@login_required
@advisor_required
def index():
    """Advisor dashboard page."""
    return render_template('advisor/index.html')
