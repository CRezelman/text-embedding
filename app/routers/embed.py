from fastapi import APIRouter, HTTPException
from app.models.embed import EmbedRequest, EmbedResponse
from app.config import client, MODEL_NAME

router = APIRouter(prefix="/embed", tags=["Embeddings"])


@router.post("", response_model=EmbedResponse)
def embed(req: EmbedRequest):
    model = req.model or MODEL_NAME
    try:
        response = client.embed(model=model, input=req.input)
        embeddings = response.embeddings
        return EmbedResponse(
            embeddings=embeddings,
            model=model,
            dimensions=len(embeddings[0]) if embeddings else 0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    