from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

# TODO: change stuff to be checklist instead of admin
# TODO: remove the line below and @admin_required
from app.decorators import admin_required

admin = Blueprint('admin', __name__)


@admin.route('/')
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')
