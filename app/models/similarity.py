from pydantic import BaseModel


class SimilarityRequest(BaseModel):
    text1: str
    text2: str
    model: str | None = None


class SimilarityResponse(BaseModel):
    text1: str
    text2: str
    score: float
    interpretation: str
    embeddings: list[list[float]] | None = None