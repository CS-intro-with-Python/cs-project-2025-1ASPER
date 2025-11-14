FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
COPY tests/ ./tests/
EXPOSE 8080
CMD ["flask", "--app", "backend.server.server", "run", "--host=0.0.0.0", "--port=8080"]