from sqlalchemy.orm import validates

from .. import db


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='application')
    # PERSONAL INFO
    legal_advisor = db.relationship('User')
    user_checklist_items = db.relationship('UserChecklistItem', backref='application', lazy=True)
