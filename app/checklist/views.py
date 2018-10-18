from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from app import db
from app.checklist.forms import (
    NewChecklistItemForm,
)
from app.models import ChecklistItem

checklist = Blueprint('checklist', __name__)

@checklist.route('/')
def index():
    """Checklist page."""
    checklist_items = ChecklistItem.query.all()
    return render_template('checklist/index.html', checklist_items=checklist_items)


@checklist.route('/add', methods=['GET', 'POST'])
def add_checklist_item():
    """Add a new checklist item."""
    form = NewChecklistItemForm()
    if form.validate_on_submit():
        checklist_item = ChecklistItem(
            title=form.title.data,
            description=form.description.data)
        db.session.add(checklist_item)
        db.session.commit()
        flash('Checklist item {} successfully created'.format(checklist_item.title),
              'form-success')
    return render_template('checklist/new_checklist_item.html', form=form)
