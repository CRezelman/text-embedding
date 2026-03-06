from fastapi import APIRouter, HTTPException
from app.models.similarity import SimilarityRequest, SimilarityResponse
from app.config import client, MODEL_NAME
import numpy as np

router = APIRouter(prefix="/similarity", tags=["Similarity"])


def cosine_similarity(a: list[float], b: list[float]) -> float:
    v1, v2 = np.array(a), np.array(b)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def interpret(score: float) -> str:
    if score >= 0.90:
        return "Nearly identical"
    elif score >= 0.75:
        return "Highly similar"
    elif score >= 0.50:
        return "Moderately similar"
    elif score >= 0.25:
        return "Loosely related"
    return "Not similar"


@router.post("", response_model=SimilarityResponse)
def similarity(req: SimilarityRequest, include_embeddings: bool = False):
    model = req.model or MODEL_NAME
    try:
        response = client.embed(model=model, input=[req.text1, req.text2])
        e1, e2 = response.embeddings[0], response.embeddings[1]
        score = round(cosine_similarity(e1, e2), 4)

        return SimilarityResponse(
            text1=req.text1,
            text2=req.text2,
            score=score,
            interpretation=interpret(score),
            embeddings=response.embeddings if include_embeddings else None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
