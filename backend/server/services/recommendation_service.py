from __future__ import annotations

from typing import List

from ..models import Movie


def get_recommendations(limit: int = 5) -> List[Movie]:
    if limit < 1:
        limit = 1
    if limit > 50:
        limit = 50

    movies = (
        Movie.query
        .order_by(Movie.rating.is_(None), Movie.rating.desc())
        .limit(limit)
        .all()
    )

    return movies
