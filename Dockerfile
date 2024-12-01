FROM python:3.11-slim

# Working directory in the container
WORKDIR /app

# Requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r /app/requirements.txt

# Copy application code into the container
COPY . /app

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]