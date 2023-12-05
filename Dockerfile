FROM python:3.11  # Or whichever version you need
WORKDIR /app
COPY backend/requirements.txt /app/
RUN pip install -r requirements.txt
COPY backend /app
