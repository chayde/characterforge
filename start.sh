#!/bin/bash
echo "Starting CharacterForge in Docker..."
docker-compose up --build -d
echo "Application started! Access it at http://localhost:8000"
