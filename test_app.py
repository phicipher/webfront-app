import pytest
from flask import template_rendered
from contextlib import contextmanager
from app import app as flask_app


@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def app():
    app = flask_app
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200

def test_health_check(client):
    response = client.get('/health', follow_redirects=True)
    assert response.status_code == 200
