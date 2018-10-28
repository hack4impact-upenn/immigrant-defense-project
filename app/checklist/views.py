from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (login_required, current_user)

from sqlalchemy.exc import IntegrityError

from app import db
from app.checklist.forms import (
    DefaultChecklistItemForm, UploadDocumentForm
)
from app.models import DefaultChecklistItem, Document, User

checklist = Blueprint('checklist', __name__)

@checklist.route('/')
def index():
    """Default checklist page."""
    default_checklist_items = DefaultChecklistItem.query.all()
    return render_template('checklist/index.html', default_checklist_items=default_checklist_items)

@checklist.route('/upload', methods=["GET", "POST"])
def upload():
    """Upload a pdf."""
    form = UploadDocumentForm()

    doc = Document.query.get(current_user.id)

    if form.validate_on_submit():
        if doc is None:
            doc = Document()
            doc.user_id = current_user.id
        
        doc.document_urls = form.file_urls.data
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('checklist.index'))

    form.file_urls.data = doc.document_urls

    return render_template('checklist/upload_document.html', form=form)


@checklist.route('/add', methods=['GET', 'POST'])
def add_default_checklist_item():
    """Add a new default checklist item."""
    form = DefaultChecklistItemForm()
    type = "Add New"
    if form.validate_on_submit():
        default_checklist_item = DefaultChecklistItem(
            title=form.title.data,
            description=form.description.data)
        db.session.add(default_checklist_item)
        db.session.commit()
        flash('Default checklist item {} successfully created'.format(default_checklist_item.title),
              'form-success')
        return render_template('checklist/edit_checklist_item.html', form=form, type=type)
    return render_template('checklist/edit_checklist_item.html', form=form, type=type)


@checklist.route('/<int:id>', methods=['GET', 'POST'])
def edit_default_checklist_item(id):
    """Edit a default checklist item's title and description."""
    default_checklist_item = DefaultChecklistItem.query.get(id)
    if default_checklist_item is None:
        abort(404)
    old_title = default_checklist_item.title
    form = DefaultChecklistItemForm()
    type = "Edit"
    if form.validate_on_submit():
        default_checklist_item.title = form.title.data
        default_checklist_item.description = form.description.data
        try:
            db.session.commit()
            flash('Default checklist item {} successfully changed.'.format(old_title),
                'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('Error Occurred. Please try again.', 'form-error')
        return render_template('checklist/edit_checklist_item.html', form=form, type=type)
    form.title.data = default_checklist_item.title
    form.description.data = default_checklist_item.description
    return render_template('checklist/edit_checklist_item.html', form=form, type=type)


@checklist.route('/<int:id>/delete')
def delete_default_checklist_item(id):
    """Deletes the default checklist item"""
    default_checklist_item = DefaultChecklistItem.query.get(id)
    if default_checklist_item is None:
        abort(404)
    db.session.delete(default_checklist_item)
    try:
        db.session.commit()
        flash('Successfully deleted default checklist item %s.' % default_checklist_item.title,
                'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error occurred. Please try again.', 'form-error')
        return redirect(url_for('checklist.index'))
    return redirect(url_for('checklist.index'))
