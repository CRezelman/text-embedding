from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import client, MODEL_NAME
from app.routers import embed, similarity


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Checking for model: {MODEL_NAME}")
    models = client.list()
    installed = [m.model for m in models.models]
    if MODEL_NAME not in installed:
        print(f"Pulling {MODEL_NAME}... this may take a while.")
        client.pull(MODEL_NAME)
        print("Model ready.")
    else:
        print(f"Model '{MODEL_NAME}' already installed.")
    yield


app = FastAPI(title="Text Embedding API", lifespan=lifespan)

app.include_router(embed.router)
app.include_router(similarity.router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/models", tags=["Health"])
def list_models():
    models = client.list()
    return {"models": [m.model for m in models.models]}
