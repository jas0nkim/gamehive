import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, SMALLINT


db = SQLAlchemy()

player_items = db.Table('player_items',
    db.Column('player_id', UUID(as_uuid = True), db.ForeignKey('players.id'), primary_key=True),
    db.Column('item_id', UUID(as_uuid = True), db.ForeignKey('items.id'), primary_key=True)
)

class Player(db.Model):
    """ database table 'players'
        columns:
            id: uuid (required)
            nickname: varchar(50) (required, max length 50)
            email: varchar(150) (required, max length 150)
            skill_point: smallint (required, default 0)
            guild_id: foreignkey (optional, guilds.id)
    """
    __tablename__ = 'players'

    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4, unique = True, nullable = False)
    nickname = db.Column(VARCHAR(length = 50), unique = True, nullable = False)
    email = db.Column(VARCHAR(length = 150), unique = True, nullable = False)
    skill_point = db.Column(SMALLINT(), nullable = False, default = 0)
    guild_id = db.Column(UUID(as_uuid = True), db.ForeignKey('guilds.id'), nullable = True)
    items = db.relationship('Item', secondary = player_items, lazy = 'subquery',
                            backref = db.backref('players', lazy = True))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Guild(db.Model):
    """ database table 'guilds'
        columns:
            id: uuid (required)
            name: varchar(50) (required, max length 50)
            country_code: varchar(3) (optional)
    """
    __tablename__ = 'guilds'

    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4, unique = True, nullable = False)
    name = db.Column(VARCHAR(length = 50), unique = True, nullable = False)
    country_code = db.Column(VARCHAR(length = 3), nullable = True)
    players = db.relationship('Player', backref = 'guild', lazy = True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Item(db.Model):
    """ database table 'items'
        columns:
            name: varchar(50) (required, max length 50)
            skill_point: smallint (required, default 0)
    """
    __tablename__ = 'items'

    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4, unique = True, nullable = False)
    name = db.Column(VARCHAR(length = 50), unique = True, nullable = False)
    skill_point = db.Column(SMALLINT(), default = 0, nullable = False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
