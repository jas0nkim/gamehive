import uuid
import pytest
import sqlalchemy
from gamehiveplayer import create_app
from gamehiveplayer.configs import TestingConfig
from gamehiveplayer.models import db

def create_test_db_if_need():
    """ Create test database 'test_gamehive' if not exists
    """
    with sqlalchemy.create_engine(TestingConfig.DB_URI).connect() as conn:
        conn.execute('commit')
        # create test database if not exists
        ex = conn.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TestingConfig.DATABASE_NAME}'")
        if ex.rowcount < 1:
            conn.execute(f'CREATE DATABASE {TestingConfig.DATABASE_NAME}')
            conn.execute('commit')

def init_db_tables():
    """ Create tables with SQLAlchemy models
    """
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()

def insert_test_data():
    """ Insert test data
    """
    with sqlalchemy.create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI).connect() as conn:
        insert_data = [
            f"""INSERT INTO guilds(id, name, country_code) VALUES('{uuid.uuid4()}', 'oguild01', 'US')""",
            f"""INSERT INTO guilds(id, name, country_code) VALUES('{uuid.uuid4()}', 'oguild02', 'CA')""",
            f"""INSERT INTO guilds(id, name, country_code) VALUES('{uuid.uuid4()}', 'oguild03', 'UK')""",
            f"""INSERT INTO guilds(id, name, country_code) VALUES('{uuid.uuid4()}', 'oguild04', 'US')""",
            f"""INSERT INTO guilds(id, name, country_code) VALUES('{uuid.uuid4()}', 'oguild05', 'CA')""",
            f"""INSERT INTO guilds(id, name) VALUES('{uuid.uuid4()}', 'oguild06')""",
            f"""INSERT INTO guilds(id, name) VALUES('{uuid.uuid4()}', 'oguild07')""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer01', 'oplayer01@mail.com', 100)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer02', 'oplayer02@mail.com', 150)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer03', 'oplayer03@mail.com', 200)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer04', 'oplayer04@mail.com', 100)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer05', 'oplayer05@mail.com', 100)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer06', 'oplayer06@mail.com', 300)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer07', 'oplayer07@mail.com', 140)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer08', 'oplayer08@mail.com', 100)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer09', 'oplayer09@mail.com', 180)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer10', 'oplayer10@mail.com', 100)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer11', 'oplayer11@mail.com', 650)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer12', 'oplayer12@mail.com', 100)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer13', 'oplayer13@mail.com', 300)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer14', 'oplayer14@mail.com', 120)""",
            f"""INSERT INTO players(id, nickname, email, skill_point) VALUES('{uuid.uuid4()}', 'oplayer15', 'oplayer15@mail.com', 340)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem01', 10)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem02', 20)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem03', 30)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem04', 10)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem05', 20)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem06', 30)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem07', 10)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem08', 20)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem09', 30)""",
            f"""INSERT INTO items(id, name, skill_point) VALUES('{uuid.uuid4()}', 'oitem10', 40)""",
        ]

        for statement in insert_data:
            conn.execute(statement)
        conn.execute('commit')

def pytest_configure(config):
    create_test_db_if_need()
    init_db_tables()
    insert_test_data()

@pytest.fixture(scope="session", autouse=True)
def client():
    """ return a Flask client (with TestingConfig)
    """
    app = create_app(TestingConfig)
    # generate flask test client
    with app.test_client() as client:
        yield client