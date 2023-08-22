# Use an official Python runtime as a parent image
#FROM python:3.8-slim-buster

# Use jupyter/base-notebook as the base image
FROM jupyter/base-notebook
# Install OpenSSH server
USER root

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD requirements.txt /app

RUN apt-get update && apt-get install -y gcc

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Expose port 22 for SSH and port 8888 for the Jupyter Notebook server
EXPOSE 22 8888

# Set the working directory to /home/jovyan (the default user in the base image)
WORKDIR /home/jovyan

# Run app.py when the container launches
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# Start the SSH server and the Jupyter Notebook server
CMD start-notebook.sh

# Copy the FastAPI application code into the container at /app
ADD . /app
# Set the working directory back to /app
WORKDIR /app
# Run app.py using uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
