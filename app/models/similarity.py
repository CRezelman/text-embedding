from pydantic import BaseModel
from typing import Literal


class SimilarityRequest(BaseModel):
    text1: str
    text2: str
    model: str | None = None

class JSONSimilarityRequest(BaseModel):
    json1: dict
    json2: dict
    model: str | None = None
    strategy: Literal["normalize", "flatten", "values_only"] = "normalize"


class SimilarityResponse(BaseModel):
    text1: str
    text2: str
    score: float
    interpretation: str
    embeddings: list[list[float]] | None = None