from .. import db


class SurveyQuestion(db.Model):
    __tablename__ = 'survey_question'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    # options = db.Column(db.PickleType)
    screen = db.Column(db.Boolean, default=False, nullable=False)
    responses = db.relationship('SurveyResponse', backref='question', lazy='dynamic')

    @staticmethod
    def generate_fake(count=5):
        from sqlalchemy.exc import IntegrityError
        from faker import Faker
        from random import choice
        fake = Faker()

        for i in range(count):
            question = SurveyQuestion(
                content=f'Question #{i + 1}',
                description=fake.sentence(),
                screen=choice([True, False]),
            )
            db.session.add(question)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class SurveyResponse(db.Model):
    __tablename__ = 'survey_response'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('survey_question.id'))
    content = db.Column(db.Text)
