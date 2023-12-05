FROM python:3.11
WORKDIR /app/backend
COPY backend/requirements.txt /app/backend/
RUN pip install -r requirements.txt
COPY backend /app/backend

