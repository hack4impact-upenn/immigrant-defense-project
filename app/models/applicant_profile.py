import random
from faker import Faker
from .. import db
from sqlalchemy.orm import validates

class ApplicantProfile(db.Model):
    __tablename__ = 'applicant_profile'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", back_populates="applicant_profile")
    # PERSONAL INFO
    phone_number = db.Column(db.String(15), index=True)
    legal_advisor = db.Column(db.ForeignKey('applicant_profile.id'))
    applicant = db.Column(db.ForeignKey('applicant_profile.id'))
    screening_responses = db.relationship('ScreeningAnswer', backref='applicant', lazy='dynamic')
