from pydantic import BaseModel
from typing import List

# request
class Input(BaseModel):
    encode_image: str

# response
class LabelMap(BaseModel):
    name: str
    color: List[int]

class Output(BaseModel):
    predict: List[List[int]]
    label_map: List[LabelMap]