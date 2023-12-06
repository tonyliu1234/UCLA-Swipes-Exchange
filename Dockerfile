# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Install MongoDB
RUN apt-get update && apt-get install -y mongodb

# Copy the current directory contents into the container at /app
COPY backend /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Give execute permissions
RUN chmod +x init.sh

# Make port 80 available to the world outside this container
EXPOSE 80
