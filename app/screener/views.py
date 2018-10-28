from flask import (
    Blueprint,
    render_template,
)
from flask_login import login_required

screener = Blueprint('screener', __name__)


# TODO: add screener_required decorator
@screener.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Screener dashboard page."""
    return render_template('screener/index.html')
