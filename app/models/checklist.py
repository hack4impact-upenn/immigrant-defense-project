from .. import db


class DefaultChecklistItem(db.Model):
    __tablename__ = 'default_checklist_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text)


class UserChecklistItem(db.Model):
    __tablename__ = 'user_checklist_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, index=True, default=False)
    applicant_profile_id = db.Column(db.ForeignKey('applicant_profile.id'))
<<<<<<< HEAD
    documents = db.relationship('Document', backref='user_checklist_item', lazy=True)

    def __repr__(self):
        return '<User Checklist Item: Title = {}, Description = {}, Completed = {}, Document = {}>'.format(self.title, self.description, self.completed, self.document)
=======
>>>>>>> fb34cbf... making relationship between checklist items and applicant profile
