FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY database/ ./database/

EXPOSE 5000

CMD ["sh", "backend/entrypoint.sh"]