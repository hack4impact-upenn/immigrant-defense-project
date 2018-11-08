from faker import Faker
from sqlalchemy.orm import validates

from .. import db


class Stage:
    UNMATCHED_PARTNER = 'Partner unmatched'
    MATCHED_PARTNER = 'Partner matched'
    COMPLETED_CHECKLIST = 'Checklist completed'
    IDP_ACCEPTED = 'Accepted IDP'
    IDP_REJECTED = 'Rejected IDP'
    MATCHED_ADVISOR = 'Legal advisor matched'

class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='application')
    stage = db.Column(db.String, default=Stage.UNMATCHED_PARTNER, nullable=False)
    legal_advisor = db.relationship('User')
    user_checklist_items = db.relationship('UserChecklistItem', backref='application', lazy=True)
    survey_responses = db.relationship('SurveyResponse', backref='application', lazy=True)

    def get_id(self):
        return self.id
