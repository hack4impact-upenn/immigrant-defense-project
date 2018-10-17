from .. import db

class ChecklistItem(db.Model):
    __tablename__ = 'checklist_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(64))
