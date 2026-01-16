# API Docs (short)

Base URL (local): `http://localhost:8080`

## Pages

- `GET /`  
  Home page (movie catalog UI)

- `GET /movie/<id>`  
  Movie detail page with HTML5 video player

- `GET /admin/login`  
  Admin login page (password: `3333`)

- `POST /admin/login`  
  Submit admin password

- `GET /admin`  
  Admin dashboard (requires admin session)

- `GET /admin/logout`  
  Clear admin session


## Auth (GitHub OAuth 2.0)

- `GET /login`  
  Redirect to GitHub OAuth (works only if `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` are set)

- `GET /authorize`  
  OAuth callback URL (set this in GitHub OAuth App)

- `GET /logout`  
  Clear user session

## JSON API

### Movies
- `GET /api/movies`  
  Returns list of movies

- `GET /api/movies/<id>`  
  Returns a single movie  
  `404` if not found

- `POST /api/movies`  
  Create a movie  
  Normal mode: requires admin session  
  Test mode (`TESTING=True`): admin check disabled

  **JSON body:**
  ```json
  {
    "title": "Movie title",
    "genre": "Action",
    "year": 2024,
    "rating": 8.7,
    "description": "Short description",
    "video_url": "/static/videos/file.mp4"
  }
  ```

  **Multipart form-data (admin upload):**
  - `title` (required)
  - `genre` (required)
  - `year` (optional)
  - `rating` (optional)
  - `description` (optional)
  - `video_url` (optional, direct file URL)
  - `video_file` (optional, `.mp4/.webm/.ogg`)

- `PUT /api/movies/<id>`  
  Update a movie (JSON). Normal mode: requires admin session.  
  `404` if not found

- `DELETE /api/movies/<id>`  
  Delete a movie. Normal mode: requires admin session.  
  `404` if not found

### Recommendations
- `GET /api/recommendations?limit=5`  
  Returns top movies (sorted by rating, unrated last)

## Response format (Movie)

```json
{
  "id": 1,
  "title": "Movie title",
  "genre": "Action",
  "year": 2024,
  "rating": 8.7,
  "description": "Short description",
  "video_url": "/static/videos/file.mp4"
}
```
