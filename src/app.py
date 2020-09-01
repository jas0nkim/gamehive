from gamehiveplayer import create_app
from gamehiveplayer.models import db

app = create_app()

def init_db():
    """ initialize database table
        WARNING: run this function will remove existing data in the tables - players, guilds, items, player_items
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
