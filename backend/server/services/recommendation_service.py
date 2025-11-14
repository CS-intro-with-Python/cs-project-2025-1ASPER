from typing import List, Dict


def get_recommendations() -> List[Dict[str, str]]:
    """A mock recommendation service. It just returns a hardcoded list. Only for now :)"""
    
    return [
        {"id": "1", "title": "The Shawshank Redemption", "genre": "Drama"},
        {"id": "2", "title": "The Godfather", "genre": "Crime"},
        {"id": "3", "title": "The Dark Knight", "genre": "Action"}
    ]