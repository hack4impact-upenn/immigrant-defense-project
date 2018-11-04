from .. import db
from . import Application


class DefaultChecklistItem(db.Model):
    __tablename__ = 'default_checklist_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text)

    @staticmethod
    def generate_fake(count=10, **kwargs):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        from faker import Faker

        fake = Faker()
        seed()
        checklist_items = []
        for i in range(count):
            item = DefaultChecklistItem(
                title=fake.word(),
                description=fake.sentence()
            )
            checklist_items.append(item)
            db.session.add(item)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        return checklist_items


class UserChecklistItem(db.Model):
    __tablename__ = 'user_checklist_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, index=True, default=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    documents = db.relationship('Document', backref='user_checklist_item', lazy=True)

    # TODO: may be changed once relations between application and user
    # are hashed out

    def __repr__(self):
        return '<User Checklist Item: Title = {}, Description = {}, Completed = {}, Document = {}>'.format(self.title, self.description, self.completed, self.document)
