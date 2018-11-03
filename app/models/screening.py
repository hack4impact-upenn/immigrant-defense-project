from .. import db


class ScreeningQuestion(db.Model):
    __tablename__ = 'screening_question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answers = db.relationship(
        'ScreeningAnswer', backref='question', lazy='dynamic')


class ScreeningAnswer(db.Model):
    __tablename__ = 'screening_answer'
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant_profile.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('screening_question.id'))
    answer = db.Column(db.Text)
