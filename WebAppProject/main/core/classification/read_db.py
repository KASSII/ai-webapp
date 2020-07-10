import plyvel
import os
from PIL import Image
import io
import pickle
import json
import base64

def load_data(db_path, start_idx, request_data_num):
    db = plyvel.DB(db_path, create_if_missing=False)

    # メタデータの読み出し
    meta_data = json.loads(db.get(b'meta_data').decode())
    task_type = meta_data["task_type"]
    train_num = meta_data["data_num"]

    # ラベルマップの読み出し
    label_map = json.loads(db.get(b'label_map').decode())
    
    # データの読み出し
    datas = []
    for idx in range(request_data_num):
        data = db.get('data{}'.format(start_idx+idx).encode('utf-8'))
        data = pickle.loads(data)
        #img = Image.open(io.BytesIO(data["img"]))
        encoded_img = base64.b64encode(data["img"])
        label = data["label"]
        data = {"img": encoded_img, "label": label}
        datas.append(data)
    return datas
    