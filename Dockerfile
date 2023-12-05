FROM python:3.11
WORKDIR /app
COPY backend/requirements.txt /app/
RUN pip install -r requirements.txt
COPY backend /app
