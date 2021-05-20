from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app(**config_overrides):
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.config['MONGODB_SETTINGS'] = {
        'db': 'app_db',
        'host': 'localhost',
        'port': 27017,
        'username': 'appUser',
        'password': 'passwordForAppUser',
        'authentication_source': 'admin'
        }

    app.config.update(config_overrides)

    db.init_app(app)

    from main.views import main_app
    app.register_blueprint(main_app)

    from menu.views import menu_app
    app.register_blueprint(menu_app)



    return app
