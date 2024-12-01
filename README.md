# Setup

## Prerequisites
- Python 3.11 or higher
- Docker

## Running Locally
1. Install dependencies
> pip install -r requirements.txt

2. Start the application
> uvicorn main:app --host 0.0.0.0 --port 8000

3. Open the API docs
Navigate to http://127.0.0.1:8000/docs#/ to explore the API endpoints.

## Running with Docker
1. Build the docker image
> docker build -t datastore-service . 

2. Run the Docker container
> docker run -p 8000:8000 datastore-service

