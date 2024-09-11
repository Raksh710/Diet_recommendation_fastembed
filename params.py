from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    query: str
    data_path: Optional[str] = "Diet_recommendation_vectorized_only_str_and_embeddings.parquet"
    threshold: Optional[float] = 0.7
    n: Optional[int] = 5