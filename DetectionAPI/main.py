from fastapi import FastAPI
import schemas
from core.task_controller import TaskController
from PIL import Image
from io import BytesIO
import base64

app = FastAPI()
task_controller = TaskController()
task_controller.load_weight()

@app.post('/predict', response_model=schemas.Output)
async def prediction(data: schemas.Input):
    encode_image = data.encode_image.split(",")[-1]          # ヘッダが付いている場合、削除したデータ部を読み込み
    # decode image
    image = Image.open(BytesIO(base64.b64decode(encode_image)))
    result, label_map = task_controller.predict(image)
    return {"predict": result, "label_map": label_map}