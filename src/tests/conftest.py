import pytest
import sqlalchemy
from gamehiveplayer import create_app
from gamehiveplayer.configs import TestingConfig
from gamehiveplayer.models import db

@pytest.fixture(scope="session", autouse=True)
def client():
    """ Flask testing client pytest fixture
    """
    with sqlalchemy.create_engine(TestingConfig.DB_URI).connect() as conn:
        conn.execute('commit')

        # create test database if not exists
        ex = conn.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TestingConfig.DATABASE_NAME}'")
        if ex.rowcount < 1:
            conn.execute(f'CREATE DATABASE {TestingConfig.DATABASE_NAME}')
            conn.execute('commit')

        # init test client
        app = create_app(TestingConfig)
        with app.test_client() as client:
            with app.app_context():
                db.drop_all()
                db.create_all()
            yield client
