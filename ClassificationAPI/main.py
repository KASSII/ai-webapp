from fastapi import FastAPI
import schemas
from core.task_controller import TaskController
from PIL import Image
from io import BytesIO
import base64

app = FastAPI()
task_controller = TaskController()
task_controller.load_weight()

@app.post('/predict')
async def prediction(data: schemas.Input):
    encode_image = data.encode_image
    # decode image
    image = Image.open(BytesIO(base64.b64decode(encode_image)))
    result = task_controller.predict(image)
    return result