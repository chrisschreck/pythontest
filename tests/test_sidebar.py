import pytest
from flask import Flask, render_template_string
from flask.testing import FlaskClient

from frontend.app import create_app

# define flask app as fixture
@pytest.fixture
def app() -> Flask:
    app = create_app()
    yield app

# define flask client as fixture
@pytest.fixture
def client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        yield client

# define mock url_for function
def mock_url_for(endpoint, **kwargs):
    return f"mock_url_for/{endpoint}"

# test sidebar rendering
def test_sidebar_rendering(client: FlaskClient, monkeypatch):
    # mock url_for
    monkeypatch.setattr("flask.url_for", mock_url_for)
    # render sidebar
    with client.application.app_context():
        with client.application.test_request_context():
            rendered_template = render_template_string("{% from 'macros/sidebar.html' import sidebar %}{{ sidebar() }}")

