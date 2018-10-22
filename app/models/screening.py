from .. import db

class ScreeningQuestion(db.Model):
    __tablename__ = 'screening_question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256))
