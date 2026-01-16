"""Unit tests for error handling in the movie service."""


def test_get_nonexistent_movie(client):
    """Requesting a non‑existent movie should return a 404."""
    response = client.get('/api/movies/9999')
    assert response.status_code == 404
    body = response.get_json()
    assert 'Movie not found' in body['error']


def test_delete_nonexistent_movie(client):
    """Deleting a non‑existent movie should return a 404."""
    response = client.delete('/api/movies/12345')
    assert response.status_code == 404
    body = response.get_json()
    assert 'Movie not found' in body['error']