#!/usr/bin/env python
import os
import subprocess
from config import Config
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from redis import Redis
from rq import Connection, Queue, Worker

from app import create_app, db
from app.models import (Application, DefaultChecklistItem, Reminder, Role,
                        SurveyQuestion, SurveyOption, SurveyResponse, User,
                        UserChecklistItem)
from app.sms import check_reminders

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.option(
    '-n',
    '--number-users',
    default=4,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    SurveyQuestion.generate_fake()
    for question in SurveyQuestion.query.all():
        SurveyOption.generate_fake(question)
    DefaultChecklistItem.generate_fake()
    User.generate_fake(count=number_users)
    Reminder.generate_fake()


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin, screener, applicant (user) and advisor user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                first_name='Admin',
                last_name='Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))
    screener_query = Role.query.filter_by(name='Screener')
    if screener_query.first() is not None:
        if User.query.filter_by(email=Config.SCREENER_EMAIL).first() is None:
            user = User(
                first_name='Screener',
                last_name='Account',
                password=Config.SCREENER_PASSWORD,
                confirmed=True,
                email=Config.SCREENER_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added screener {}'.format(user.full_name()))
    advisor_query = Role.query.filter_by(name='Advisor')
    if advisor_query.first() is not None:
        if User.query.filter_by(email=Config.ADVISOR_EMAIL).first() is None:
            user = User(
                first_name='Advisor',
                last_name='Account',
                password=Config.ADVISOR_PASSWORD,
                confirmed=True,
                email=Config.ADVISOR_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added screener {}'.format(user.full_name()))
    user_query = Role.query.filter_by(name='User')
    if user_query.first() is not None:
        if User.query.filter_by(email=Config.USER_EMAIL).first() is None:
            user = User(
                first_name='Applicant',
                last_name='Account',
                password=Config.USER_PASSWORD,
                confirmed=True,
                email=Config.USER_EMAIL)
            user.application = Application()
            db.session.add(user)
            db.session.commit()
            print('Added applicant {}'.format(user.full_name()))


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    conn = Redis(
        host=app.config['RQ_DEFAULT_HOST'],
        port=app.config['RQ_DEFAULT_PORT'],
        db=0,
        password=app.config['RQ_DEFAULT_PASSWORD'])

    # Initialize background scheduler for SMS reminders
    scheduler = BackgroundScheduler()
    # TODO change start_date once SMS reminders properly tested
    # scheduler.add_job(check_reminders, 'interval', start_date=datetime.now(), minutes=1)
    # scheduler.start()

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()
