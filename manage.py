# server/manage.py

import os
import random
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from populate import companies
from app import db, create_app
from app.models import (
    Company,
    Founder,
    User,
    Sale,
    Traffic,
    Customer,
    Email
)

app = create_app(config_name=os.environ.get('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def createdb():
    """Creates the db tables"""
    db.create_all()
    db.session.commit()


@manager.command
def dropdb():
    """Drop all db tables"""
    db.drop_all()


@manager.command
def resetdb():
    """Reset all db tables"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def populate():
    """Populate some data"""
    db.drop_all()
    db.create_all()
    staff = User(
        name="Staff",
        password="test",
        email="staff@brandery.org",
        staff=True)

    staff.save()

    for company in companies:
        new_company = Company(
            name=company['name'],
            website=company['website'],
            bio=company['bio']
        )

        print('Saving company', new_company)

        new_company.save()

        for _ in range(7):
            # Saving random metrics
            Sale(
                company_id=new_company.id, value=random.randint(0, 100)).save()
            Customer(
                company_id=new_company.id, value=random.randint(0, 100)).save()
            Traffic(
                company_id=new_company.id, value=random.randint(0, 100)).save()
            Email(
                company_id=new_company.id, value=random.randint(0, 100)).save()

        for founder in company['founders']:
            new_founder = Founder(
                name=founder['name'],
                email=founder['email'],
                role=founder['role'],
                company_id=new_company.id
            )

            print('Saving founder', founder)

            new_founder.save()

    db.session.commit()


@manager.command
def test(type=""):
    """Run the unit tests without code coverage."""
    try:
        tests = unittest.TestLoader().discover(
            f'tests/{type}',
            pattern='test*.py'
        )
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1
    except ImportError:
        print("There is no test like that!")


if __name__ == "__main__":
    manager.run()