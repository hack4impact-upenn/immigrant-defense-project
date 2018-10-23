from .. import db


class Documents(db.Model):
    __tablename__ = 'documents'
    user_id = db.Column(db.Integer, primary_key=True)
    document_urls = db.Column(db.Text)
