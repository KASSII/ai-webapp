import os
import json
from PIL import Image
import io
import base64

def load_data(dataset_path, start_idx, request_data_num):
    # ラベルマップの読み込み
    with open(os.path.join(dataset_path, "label_map.json")) as f:
        label_map = json.load(f)
    
    # データの読み込み
    datas = []
    with open(os.path.join(dataset_path, "data.list"), "r") as f:
        for idx, line in enumerate(f):
            if idx < start_idx:
                continue
            if idx >= start_idx+request_data_num:
                break

            # 画像の読み込み
            img_path, label = line.split(" ")
            img = Image.open(os.path.join(dataset_path, img_path))
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            encoded_img = base64.b64encode(buffered.getvalue())

            # ラベル名の取得
            label_name = label_map[int(label)]

            data = {"idx": idx, "img": encoded_img, "label": label_name}
            datas.append(data)
    return datas