from flask import Flask
from gamehiveplayer.configs import DefaultConfig

def create_app(config_class=DefaultConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from gamehiveplayer.models import db
    db.init_app(app)

    from gamehiveplayer.main.routes import main
    from gamehiveplayer.players.routes import players
    from gamehiveplayer.guilds.routes import guilds
    from gamehiveplayer.items.routes import items
    app.register_blueprint(main)
    app.register_blueprint(players)
    app.register_blueprint(guilds)
    app.register_blueprint(items)

    return app
