# Use a slim Python image
FROM python:3.11-slim

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/mas

# Uncomment below for production later when main.py is available
# Run the application (ensure path is correct)
#### CMD ["python", "/app/mas/main.py"]

# For development, run a Python interactive shell
CMD ["python"]

#main.py controlls runtime of python logic