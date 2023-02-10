# Use an official Python runtime as the base image
FROM python:3.9.1-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the required files to the container
COPY . /app

# Install the required packages
RUN pip install --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Run the Flask app
CMD python Main.py