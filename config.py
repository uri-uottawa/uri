import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'this-really-needs-to-be-changed'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:polo@localhost/uridb')
	HASH_ROUNDS = 100000
	SQLALCHEMY_ECHO = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
	DEBUG = False


class StagingConfig(Config):
	DEVELOPEMENT = True
	DEBUG = True

class DevelopementConfig(Config):
	DEVELOPEMENT = True
	DEBUG = True

class SecurityConfig(Config):
	UPLOAD_FOLDER = './static/uploads'
	SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'
	SECURITY_LOGIN_URL = '/login'
	SECURITY_LOGOUT_URL = '/logout'
	SECURITY_REGISTERABLE = True
	SECURITY_REGISTER_URL = '/signup'
	SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.html'
	# SECURITY_POST_REGISTER_VIEW = '/'
	SECURITY_USER_IDENTITY_ATTRIBUTES = 'email'
	# SECURITY_POST_LOGIN_VIEW = '/uri/home'
	# SECURITY_POST_LOGOUT_VIEW = '/'

class EmailConfig(Config):
	SECURITY_EMAIL_SENDER = 'uri.uottawa@gmail.com'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'uri.uottawa@gmail.com'
	MAIL_PASSWORD = 'xxxxxxxxxxxxxxxxxxxxxxxx'


class TestingConfig(Config):
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:polo@localhost/uridb')
	# Since we want our tests to run quickly
	# we turn this down - the hashing is stil done
	# but the time-consuming part is left out
	HASH_ROUNDS = 1
