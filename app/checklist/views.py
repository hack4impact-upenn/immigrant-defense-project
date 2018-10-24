from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy.exc import IntegrityError

from app import db
from app.checklist.forms import (
    ChecklistItemForm, UploadDocumentForm
)
from app.models import ChecklistItem

checklist = Blueprint('checklist', __name__)

@checklist.route('/')
def index():
    """Checklist page."""
    checklist_items = ChecklistItem.query.all()
    return render_template('checklist/index.html', checklist_items=checklist_items)

@checklist.route('/upload', methods=["GET", "POST"])
def upload():
    """Upload a pdf."""
    form = UploadDocumentForm()
    return render_template('checklist/upload_document.html', form=form)


@checklist.route('/add', methods=['GET', 'POST'])
def add_checklist_item():
    """Add a new checklist item."""
    form = ChecklistItemForm()
    type = "Add New"
    if form.validate_on_submit():
        checklist_item = ChecklistItem(
            title=form.title.data,
            description=form.description.data)
        db.session.add(checklist_item)
        db.session.commit()
        flash('Checklist item {} successfully created'.format(checklist_item.title),
              'form-success')
        return render_template('checklist/edit_checklist_item.html', form=form, type=type)
    return render_template('checklist/edit_checklist_item.html', form=form, type=type)


@checklist.route('/<int:id>', methods=['GET', 'POST'])
def edit_checklist_item(id):
    """Edit a checklist item's title and description."""
    checklist_item = ChecklistItem.query.get(id)
    if checklist_item is None:
        abort(404)
    old_title = checklist_item.title
    form = ChecklistItemForm()
    type = "Edit"
    if form.validate_on_submit():
        checklist_item.title = form.title.data
        checklist_item.description = form.description.data
        try:
            db.session.commit()
            flash('Checklist item {} successfully changed.'.format(old_title),
                'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('Error Occurred. Please try again.', 'form-error')
        return render_template('checklist/edit_checklist_item.html', form=form, type=type)
    form.title.data = checklist_item.title
    form.description.data = checklist_item.description
    return render_template('checklist/edit_checklist_item.html', form=form, type=type)


@checklist.route('/<int:id>/delete')
def delete_checklist_item(id):
    """Deletes the checklist item"""
    checklist_item = ChecklistItem.query.get(id)
    if checklist_item is None:
        abort(404)
    db.session.delete(checklist_item)
    try:
        db.session.commit()
        flash('Successfully deleted checklist item %s.' % checklist_item.title,
                'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error occurred. Please try again.', 'form-error')
        return redirect(url_for('checklist.index'))
    return redirect(url_for('checklist.index'))
