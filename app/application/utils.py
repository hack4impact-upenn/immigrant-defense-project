from flask_rq import get_queue

from app.email import send_email

def send_rejection_email(user):
	get_queue().enqueue(
        send_email,
        recipient=user.email,
        subject='Update to Immigrant Defense Project Application',
        template='account/email/rejection_email.html',
        user=user,
    )

def send_acceptance_email(user):
	get_queue().enqueue(
        send_email,
        recipient=user.email,
        subject='Update to Immigrant Defense Project Application',
        template='account/email/acceptance_email.html',
        user=user,
    )

