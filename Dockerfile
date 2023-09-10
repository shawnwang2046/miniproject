# Use the official fastapi image from tiangolo
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set the working directory in the container
WORKDIR /app

# Update apt package list and install sqlite3
RUN apt-get update && apt-get install -y sqlite3

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app /app
COPY ./tests /app/tests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
