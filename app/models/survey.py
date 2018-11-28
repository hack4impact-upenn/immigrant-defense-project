from sqlalchemy.exc import IntegrityError
from faker import Faker
import random

from .. import db


class SurveyQuestion(db.Model):
    __tablename__ = 'survey_question'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, unique=True, nullable=False)
    content = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    options = db.relationship('SurveyOption', backref='question', lazy='dynamic')

    @staticmethod
    def next_rank():
        return SurveyQuestion.query.count() + 1

    @staticmethod
    def generate_fake(count=5):
        fake = Faker()
        for i in range(count):
            question = SurveyQuestion(
                content=f'Question #{i + 1}',
                description=fake.sentence(),
                rank=SurveyQuestion.next_rank(),
            )
            db.session.add(question)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class SurveyOptionAction():
    COMPLETED = -2      # survey is completed
    STOP = -1           # survey stops; applicant cannot proceed to make an account
    CONTINUE = 0        # default


class SurveyOption(db.Model):
    __tablename__ = 'survey_option'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('survey_question.id'))
    content = db.Column(db.String, nullable=False)
    next_action = db.Column(db.Integer, nullable=False, default=SurveyOptionAction.CONTINUE)
    stop_description = db.Column(db.String)

    @staticmethod
    def generate_fake(question, count=4):
        fake = Faker()
        for i in range(random.randint(2, count)):
            option = SurveyOption(
                question_id=question.id,
                content=f'Option #{i + 1} for {question.content}',
                stop_description=fake.sentence(),
            )
            db.session.add(option)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def action_text(self):
        if self.next_action == SurveyOptionAction.COMPLETED:
            return 'Submit survey'
        elif self.next_action == SurveyOptionAction.STOP:
            if len(self.stop_description) > 30:
                stop_description = self.stop_description[:30].strip() + '...'
            else:
                stop_description = self.stop_description
            return f'End survey ({stop_description})'
        elif self.next_action == SurveyOptionAction.CONTINUE:
            return 'Continue to next question'
        else:
            question = SurveyQuestion.query.get(self.next_action)
            if len(question.content) > 30:
                question_content = question.content[:30].strip() + '...'
            else:
                question_content = question.content
            return f'Skip to "{question_content}"'


class SurveyResponse(db.Model):
    __tablename__ = 'survey_response'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    question_content = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)

    @staticmethod
    def generate_fake(application):
        for question in SurveyQuestion.query.all():
            options = SurveyOption.query.filter_by(question_id=question.id).all()
            response = SurveyResponse(
                application_id=application.id,
                question_content=question.content,
                content=random.choice(options).content,
            )
            db.session.add(response)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
