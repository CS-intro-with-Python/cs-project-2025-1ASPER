FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV FLASK_APP=backend.server.server
ENV FLASK_ENV=production

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY tests/ ./tests/


CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
