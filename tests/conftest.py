"""Pytest fixtures for the movie recommendation service tests.

This file defines application and client fixtures for testing. The
application fixture uses an in‑memory SQLite database to avoid
interfering with any production data. Tables are created and
destroyed around each test session.
"""

import os
import pytest

from backend.server.server import create_app
from backend.server.models import db, Movie


@pytest.fixture
def app():
    """Create a Flask app configured for testing.

    The app uses an in‑memory SQLite database and has TESTING enabled.
    """
    # Override the database URI to use an in‑memory SQLite database
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    os.environ['SQLALCHEMY_ECHO'] = 'false'
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.app_context():
        db.create_all()
        yield app
        # Clean up / reset resources here
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the Flask app."""
    return app.test_client()