from .. import db


class ScreeningQuestion(db.Model):
    __tablename__ = 'screening_question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answers = db.relationship('ScreeningAnswer', backref='question', lazy='dynamic')

class ScreeningAnswer(db.Model):
    __tablename__ = 'screening_answer'
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    applicant = db.Column(db.Integer, db.ForeignKey('applicant_profile.id'))
    question = db.Column(db.Integer, db.ForeignKey('screening_question.id'))
=======
    applicant_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('screening_question.id'))
>>>>>>> a5fe76fbf5535d6199f9330a00b7070181f873ff
    answer = db.Column(db.Text)
