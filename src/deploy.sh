#!/bin/bash
# Production deployment script for Vertex Training Platform

echo "Starting Vertex Training Platform..."
cd "$(dirname "$0")"
source venv/bin/activate
export FLASK_ENV=production
python src/main.py
