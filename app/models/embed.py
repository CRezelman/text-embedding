from pydantic import BaseModel


class EmbedRequest(BaseModel):
    input: str | list[str]
    model: str | None = None


class EmbedResponse(BaseModel):
    embeddings: list[list[float]]
    model: str
    dimensions: int