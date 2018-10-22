from twilio.rest import Client
import os
import unittest


class SMSTest(unittest.TestCase):

    def test_send_sms(self):
        phone_no = os.environ.get('PHONE_NO') or None
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID') or None
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN') or None
        twilio_phone = os.environ.get('TWILIO_PHONE_NO') or None

        self.assertTrue(None not in [phone_no, account_sid, auth_token, twilio_phone])

        # Send SMS
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="Test SMS from IDP application",
            to=phone_no,
            from_=twilio_phone,
        )
        print(message.sid)
