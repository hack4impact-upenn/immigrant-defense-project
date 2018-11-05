from .. import db
from . import Application

class ScreeningQuestion(db.Model):
    __tablename__ = 'screening_question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answers = db.relationship('ScreeningAnswer', backref='screening_question', lazy='dynamic')

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from faker import Faker

        fake = Faker()
        for i in range(count):
            item = ScreeningQuestion(
                question=fake.sentence()
            )
            db.session.add(item)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class ScreeningAnswer(db.Model):
    __tablename__ = 'screening_answer'
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('screening_question.id'))
    answer = db.Column(db.Text)
