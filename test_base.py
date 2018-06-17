from flask_testing import TestCase
from routes import app, db

class BaseTest(TestCase):
    """ A base test case for the app """

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
