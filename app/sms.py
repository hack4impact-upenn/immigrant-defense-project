import os
import re
from datetime import datetime, timedelta

from twilio.rest import Client

from app import create_app, db
from app.models import Reminder


def format_phone(number):
    return '+1' + re.sub('^[0-9]', '', number) if number[0] != '+' else number


def next_timestamp(dt):
    """
    Rounds datetime to the next hour.
    """
    return dt + timedelta(hours=1) if dt.minute or dt.second else dt


def send(reminder):
    # TODO: replace fake phone number later
    phone_number = os.environ.get('PHONE_NO')
    if not phone_number:
        print('Add PHONE_NO to config.env file.')

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID') or None
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN') or None
    twilio_phone = os.environ.get('TWILIO_PHONE_NO') or None
    if None in [account_sid, auth_token, twilio_phone]:
        print('Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NO to config.env file.')
        return

    client = Client(account_sid, auth_token)

    print(f'Send reminder "{reminder.content}" to {format_phone(phone_number)}')
    client.messages.create(
        to=format_phone(phone_number),
        from_=twilio_phone,
        body=reminder.content
    )

def check_reminders():
    """
    Calls send_reminder for each reminder that should be sent within the next hour.
    """
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        next = next_timestamp(datetime.now())
        reminders = []
        for reminder in Reminder.query.filter_by(date=next.date(), sent=False).all():
            if reminder.time.hour == next.hour:
                reminders.append(reminder)
                reminder.sent = True
                db.session.add(reminder)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    print(f'Could not send reminder {reminder.title}')

        # TODO: replace fake phone number later
        phone_number = os.environ.get('PHONE_NO')
        if not phone_number:
            print('Add PHONE_NO to config.env file.')

        account_sid = os.environ.get('TWILIO_ACCOUNT_SID') or None
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN') or None
        twilio_phone = os.environ.get('TWILIO_PHONE_NO') or None
        if None in [account_sid, auth_token, twilio_phone]:
            print('Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NO to config.env file.')
            return

        client = Client(account_sid, auth_token)

        # Send SMS
        for reminder in reminders:
            print(f'Send reminder "{reminder.content}" to {format_phone(phone_number)}')
            client.messages.create(
                to=format_phone(phone_number),
                from_=twilio_phone,
                body=reminder.content
            )
