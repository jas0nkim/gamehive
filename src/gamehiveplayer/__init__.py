from flask import Flask

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/gamehive'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from gamehiveplayer.models import db
    db.init_app(app)

    from gamehiveplayer.main.routes import main
    app.register_blueprint(main)

    return app
