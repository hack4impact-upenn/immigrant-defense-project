from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import screener_required

screener = Blueprint('screener', __name__)


@screener.route('/', methods=['GET', 'POST'])
@login_required
@screener_required
def index():
    """Screener dashboard page."""
    return render_template('screener/index.html')
