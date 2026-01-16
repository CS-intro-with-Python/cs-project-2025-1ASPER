"""Unit tests for input validation in the movie service."""

def test_create_movie_missing_title(client):
    """POST without title should return 400 Bad Request."""
    response = client.post('/api/movies', json={'genre': 'Drama'})
    assert response.status_code == 400
    assert 'Missing title or genre' in response.get_json()['error']


def test_create_movie_missing_genre(client):
    """POST without genre should return 400 Bad Request."""
    response = client.post('/api/movies', json={'title': 'Test Movie'})
    assert response.status_code == 400
    assert 'Missing title or genre' in response.get_json()['error']