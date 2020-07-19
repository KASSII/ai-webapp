from pydantic import BaseModel
from typing import List

# request
class Input(BaseModel):
    encode_images: List[str]

# response
class Pred(BaseModel):
    prob: float
    label: str

class Output(BaseModel):
    prediction: List[Pred]