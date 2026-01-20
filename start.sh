#!/bin/bash

# Initialize and seed database on first run
python -m app.seed

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
