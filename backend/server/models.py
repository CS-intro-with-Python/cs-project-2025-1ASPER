"""Database models for the movie recommendation service.

This module defines the SQLAlchemy models used by the application. It
exposes a `db` instance that should be initialized with the Flask app
in ``server.py``. Models defined here include a simple ``Movie`` table
with fields suitable for storing basic information and an optional
rating. Additional models can be added here as the project grows.
"""

from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    """Represents a movie in the database.

    Movies have a title and genre, both of which are required. The
    ``year`` and ``rating`` fields are optional. The ``id`` column is
    automatically generated and serves as the primary key.
    """

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    # A longer plot description. Optional – not every movie must have one.
    description = db.Column(db.Text, nullable=True)
    # A URL or path pointing to the video file or stream. Optional.
    video_url = db.Column(db.String(512), nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - representation not needed in tests
        return f"<Movie id={self.id} title={self.title}>"

    def to_dict(self) -> dict[str, object]:
        """Serialize the movie instance into a plain dictionary.

        :returns: A dictionary representation of the movie suitable for
            JSON serialization via :func:`flask.jsonify`.
        """
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating,
            "description": self.description,
            "video_url": self.video_url,
        }
