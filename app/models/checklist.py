from .. import db

class DefaultChecklistItem(db.Model):
    __tablename__ = 'default_checklist_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(256))

