from .. import db


class Document(db.Model):
    __tablename__ = 'document'
    user_id = db.Column(db.Integer, primary_key=True)
    document_urls = db.Column(db.Text)
    checklist_item = db.Column(db.foreignKey('UserChecklistItem.id'))
