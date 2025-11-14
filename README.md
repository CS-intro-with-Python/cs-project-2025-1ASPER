# Movie Recommendation System

[![CI Check](https://github.com/1ASPER/cs-project-2025-1ASPER/actions/workflows/ci.yml/badge.svg)](https://github.com/1ASPER/cs-project-2025-1ASPER/actions/workflows/ci.yml)

This project is a mock movie recommendation service built for the Client-Server Application course. It demonstrates a complete, production-ready CI/CD pipeline using Flask, Docker, GitHub Actions, and Railway.


## Demo
The application is automatically deployed from the `main` branch after passing all CI checks and is publicly available at:

**[https://cs-project-2025-1asper-production.up.railway.app/](https://cs-project-2025-1asper-production.up.railway.app/)**


## Features

* `/`: A simple HTML welcome page that serves as the application's UI.
* `/api/recommendations`: A JSON API endpoint that returns a hardcoded list of movie recommendations.


## Tech stack
* **Backend:** **Python 3.11** with **Flask**
* **Containerization:** **Docker**
* **Continuous Integration (CI):** **GitHub Actions**
* **Continuous Deployment (CD):** **Railway.app**


## Project Structure

```text
.
├── .github/workflows/
│   └── ci.yml                              # GitHub actions
├── backend/
│   ├── server/
│   │   ├── __init__.py
│   │   ├── server.py                        # Main app with routes
│   │   └── services/
│   │       ├── __init__.py  
│   │       └── recommendation_service.py    # Main logic
│   └── templates/
│       └── index.html
├── tests/
│   └── client.py                            # CI tests
├── Dockerfile
├── requirements.txt
└── README.md
```


## Running locally
First, you must have [DOCKER](https://www.docker.com/get-started) installed to run this project locally.

### 1. Build the docker image

From the project's root directory build the image using the exact name:

```bash
docker build -t asper/docker_reco .
```

### 2. Run the container

Run the container with port 8080 on your PC to port 8080 inside the container.

```bash
docker run -d --name movie-server -p 8080:8080 asper/docker_reco
```


### 3. Find the local host
Once the container is running you can find the app in your browser:

* UI: http://localhost:8080/
* API: http://localhost:8080/api/recommendations

## Running tests

The project includes an integration test client 'tests/client.py' that checks the UI and API. To run it the container must be running. Then, execute the following command:

```bash
docker exec movie-server python tests/client.py
```


## How this project updates?
This project do all the stuff automatically!

1.  **Push to GitHub:** When I save new code to GitHub, a process (GitHub Action) starts

2.  **CI (GitHub Actions):** This process builds the Docker image and runs the `tests/client.py` test. This checks that the new code works and did not break the project

3.  **CD (Railway):** Railway checks if the CI test passed.
    * If the test passes, Railway builds the new code and updates the live website
    * If the test fails, Railway stops. The old, working website stays live
