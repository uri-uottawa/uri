import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from routes import app, db

app.config.from_object('config.StagingConfig')


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
