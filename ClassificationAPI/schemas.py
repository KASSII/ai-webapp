from pydantic import BaseModel
from typing import List

# request
class Input(BaseModel):
    encode_image: str

# response