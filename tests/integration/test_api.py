"""Integration tests for API endpoints of the movie service."""

import json


def test_create_and_retrieve_movie(client):
    """Ensure that a movie can be created and then retrieved via the API."""
    # Create a movie
    payload = {
        'title': 'Inception',
        'genre': 'Sci-Fi',
        'year': 2010,
        'rating': 8.8,
    }
    create_resp = client.post('/api/movies', json=payload)
    assert create_resp.status_code == 201
    data = create_resp.get_json()
    movie_id = data['id']

    # Retrieve the same movie
    get_resp = client.get(f'/api/movies/{movie_id}')
    assert get_resp.status_code == 200
    movie = get_resp.get_json()
    assert movie['title'] == payload['title']
    assert movie['genre'] == payload['genre']
    assert movie['year'] == payload['year']
    assert movie['rating'] == payload['rating']


def test_update_and_delete_movie(client):
    """Ensure that movies can be updated and deleted via the API."""
    # Create a movie to update and delete
    payload = {'title': 'Matrix', 'genre': 'Action'}
    create_resp = client.post('/api/movies', json=payload)
    assert create_resp.status_code == 201
    movie_id = create_resp.get_json()['id']

    # Update the movie's rating
    update_resp = client.put(f'/api/movies/{movie_id}', json={'rating': 9.0})
    assert update_resp.status_code == 200
    updated = update_resp.get_json()
    assert updated['rating'] == 9.0

    # Delete the movie
    delete_resp = client.delete(f'/api/movies/{movie_id}')
    assert delete_resp.status_code == 200
    assert delete_resp.get_json()['message'] == 'Movie deleted'

    # Ensure it no longer exists
    not_found_resp = client.get(f'/api/movies/{movie_id}')
    assert not_found_resp.status_code == 404