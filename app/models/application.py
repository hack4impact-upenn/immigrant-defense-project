from .. import db
from sqlalchemy.orm import validates

class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='application')
    # PERSONAL INFO
    phone_number = db.Column(db.String(15), index=True)
    legal_advisor = db.relationship('User')
    user_checklist_items = db.relationship('UserChecklistItem', backref='application', lazy=True)

    @staticmethod
    def generate_fake():
        from faker import Faker
        return Application(phone_number=Faker().phone_number())
