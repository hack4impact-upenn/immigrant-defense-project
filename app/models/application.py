import random
from faker import Faker
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

    def generate_fake():
        return Application(phone_number='+12345678900')
