import os
import ollama

MODEL_NAME = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:8b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = ollama.Client(host=OLLAMA_HOST)