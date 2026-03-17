import pytest
import os
import sys

# Ensure project root is on sys.path when pytest runs
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend import create_app, db


@pytest.fixture
def app():
    # pass test config so the app uses sqlite in-memory for tests
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.json['status'] == 'ok'
