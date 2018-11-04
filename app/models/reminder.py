import datetime
import random

from .. import db


class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    content = db.Column(db.String, index=True)
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Time, index=True)
    sent = db.Column(db.Boolean, index=True, default=False)

    def format_date(self):
        return self.date.strftime('%M/%D/%Y')

    def format_time(self):
        return self.time.strftime('%-I:%M %p')

    @staticmethod
    def generate_fake(count=3):
        for i in range(1, count + 1):
            # randomly generate a reminder datetime to be within 1-3 minutes from now
            soon = datetime.datetime.now() + datetime.timedelta(
                seconds=random.randint(60, 180))
            reminder = Reminder(
                title=f'Reminder {i}',
                content=f'Please make sure to complete Task #{i}.',
                date=soon.date(),
                time=soon.time())
            db.session.add(reminder)
            try:
                db.session.commit()
            except:
                db.session.rollback()
