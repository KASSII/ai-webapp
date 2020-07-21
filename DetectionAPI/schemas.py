from pydantic import BaseModel
from typing import List

# request
class Input(BaseModel):
    encode_image: str

# response
class Pred(BaseModel):
    bbox: List[int]
    label: str
    score: float

class Output(BaseModel):
    predict: List[Pred]