from sqlalchemy.orm import validates

from .. import db

from faker import Faker


class Stage:
    UNMATCHED_PARTNER = 'unmatched_partner'
    MATCHED_PARTNER = 'matched_partner'
    COMPLETED_CHECKLIST = 'completed_checklist'
    IDP_ACCEPTED = 'idp_accepted'
    IDP_REJECTED = 'idp_rejected'
    MATCHED_ADVISOR = 'matched_legal_advisor'

class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='application')
    stage = db.Column(db.String, default=Stage.UNMATCHED_PARTNER, nullable=False)
    legal_advisor = db.relationship('User')
    user_checklist_items = db.relationship('UserChecklistItem', backref='application', lazy=True)
    screening_answer = db.relationship('ScreeningAnswer', backref='application', lazy=True)

    @staticmethod
    def generate_fake(count=10, **kwargs):
        fake = Faker()
        for i in range(count):
            application = Application(
                phone_number=fake.phone_number(),
            )
            db.session.add(application)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def generate_one_fake():
        fake = Faker()
        application = Application(
            phone_number=fake.phone_number(),
        )
        db.session.add(application)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return application

    def get_id(self):
        return self.id
