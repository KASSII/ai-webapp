import os
import glob
import json
from PIL import Image
from io import BytesIO
import base64
import urllib.request

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

        url = "http://127.0.0.1:8001/predict" 
        method = "POST"
        headers = {"Content-Type" : "application/json"}
        request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
        print(response_body)
