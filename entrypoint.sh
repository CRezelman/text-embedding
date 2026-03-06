#!/bin/bash
set -e

# Start Ollama in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until curl -sf http://localhost:11434 > /dev/null 2>&1; do
  sleep 1
done
echo "Ollama is ready."

# Start FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000