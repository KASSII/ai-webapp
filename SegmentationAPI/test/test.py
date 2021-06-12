import os
import glob
import json
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import urllib.request

def annot2mask(annot, label_map):
    """
        アノテーション画像（ラベル値）からマスク画像（RGB）への変換

    Parameters
    ----------
    annot: PIL Image
        アノテーション画像データ（ラベル値）
    label_map: list
        マスク画像データ（RGB形式）

    Returns
    -------
    PIL Image
        アノテーション画像データ（ラベル値）
    """
    height, width = annot.shape
    mask = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    for idx, label in enumerate(label_map):
        color = np.asarray(label["color"])
        mask[(annot == idx)] = color
    return Image.fromarray(np.uint8(mask))

if __name__ == '__main__':
    image_pathes = glob.glob("samples/*.jpg")
    image_pathes.sort()
    
    for image_path in image_pathes:
        with open(image_path, "rb") as f:
            encode_image = base64.b64encode(f.read())
        encode_image = encode_image.decode('utf-8')
        obj = {
            "encode_image": encode_image
        }
        json_data = json.dumps(obj).encode("utf-8")

        url = "http://127.0.0.1:8003/predict" 
        method = "POST"
        headers = {"Content-Type" : "application/json"}
        request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
        
        response_body = json.loads(response_body)
        annot = np.asarray(response_body["predict"])
        label_map = response_body["label_map"]
        print(annot.shape)
        print(label_map)

        mask = annot2mask(annot, label_map)
        mask.show()
