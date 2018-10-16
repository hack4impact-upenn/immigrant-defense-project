from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

checklist = Blueprint('checklist', __name__)

@checklist.route('/')
def index():
    """Checklist page."""
    return render_template('checklist/index.html')
