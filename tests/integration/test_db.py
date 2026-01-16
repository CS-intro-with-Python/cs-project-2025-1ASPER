"""Integration tests verifying database operations."""

from backend.server.models import db, Movie


def test_database_inserts_work(app):
    """Ensure that direct database operations succeed."""
    with app.app_context():
        # Insert a new movie directly via SQLAlchemy session
        m = Movie(title="Test DB", genre="Test Genre", year=2021, rating=7.0)
        db.session.add(m)
        db.session.commit()
        assert m.id is not None
        # Query back and verify
        retrieved = Movie.query.filter_by(title="Test DB").first()
        assert retrieved is not None
        assert retrieved.genre == "Test Genre"