from fastapi import APIRouter, HTTPException
from app.models.similarity import JSONSimilarityRequest, SimilarityRequest, SimilarityResponse
from app.config import client, MODEL_NAME
import numpy as np
import json

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


def serialize_json(obj: dict, strategy: str) -> str:
    if strategy == "normalize":
        return json.dumps(obj, sort_keys=True, ensure_ascii=False)
    elif strategy == "values_only":
        return extract_values(obj)
    elif strategy == "flatten":
        return flatten_to_text(obj)
    return json.dumps(obj)

def extract_values(obj) -> str:
    if isinstance(obj, dict):
        return " ".join(extract_values(v) for v in obj.values())
    elif isinstance(obj, list):
        return " ".join(extract_values(i) for i in obj)
    return str(obj)

def flatten_to_text(obj: dict, prefix: str = "") -> str:
    parts = []
    for k, v in obj.items():
        label = f"{prefix}{k}".replace("_", " ")
        if isinstance(v, dict):
            parts.append(flatten_to_text(v, prefix=f"{label} "))
        elif isinstance(v, list):
            parts.append(f"{label} is {', '.join(str(i) for i in v)}")
        else:
            parts.append(f"{label} is {v}")
    return ". ".join(parts)


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


@router.post("/json", response_model=SimilarityResponse)
def json_similarity(req: JSONSimilarityRequest):
    model = req.model or MODEL_NAME
    try:
        t1 = serialize_json(req.json1, req.strategy)
        t2 = serialize_json(req.json2, req.strategy)

        response = client.embed(model=model, input=[t1, t2])
        e1, e2 = response.embeddings[0], response.embeddings[1]
        score = round(cosine_similarity(e1, e2), 4)

        return SimilarityResponse(
            text1=t1,
            text2=t2,
            score=score,
            interpretation=interpret(score),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
