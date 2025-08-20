#!/bin/bash

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example"
    cp .env.example .env
    echo "Please update the .env file with your actual configuration"
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the server
echo "Starting server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000