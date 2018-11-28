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

    def truncated_content(self, max_length=30, suffix='...'):
        if len(self.content) <= max_length:
            return self.content
        else:
            return ' '.join(self.content[:max_length + 1].split(' ')[0:-1]) + suffix


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
            return f'End survey ({self.truncated_stop_description()})'
        elif self.next_action == SurveyOptionAction.CONTINUE:
            return 'Continue to next question'
        else:
            question = SurveyQuestion.query.get(self.next_action)
            return f'Skip to "{question.truncated_content()}"'

    def truncated_stop_description(self, max_length=60, suffix='...'):
        if len(self.stop_description) <= max_length:
            return self.stop_description
        else:
            return ' '.join(self.stop_description[:max_length + 1].split(' ')[0:-1]) + suffix



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
