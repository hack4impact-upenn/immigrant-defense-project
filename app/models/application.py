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
    stage = db.Column(db.String, default=Stage.UNMATCHED_PARTNER, nullable=False)

    legal_advisor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    legal_advisor = db.relationship('User', foreign_keys=[legal_advisor_id], backref='client_applications')

    partner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parner = db.relationship('User', foreign_keys=[partner_id], backref='partner_applications')

    checklist_items = db.relationship('UserChecklistItem', backref='application', lazy=True)
    survey_responses = db.relationship('SurveyResponse', backref='application', lazy=True)

    def get_id(self):
        return self.id
