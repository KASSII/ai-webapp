import os
import json
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import models

from . import transform
from . import model

class TaskController():
    def __init__(self):
        # Transformerを定義
        size = 475
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)
        self.transformer = transform.SegmentationTransform(size, mean, std)
    
        # ネットワークモデルの作成
        label_map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/label_map.json")
        with open(label_map_path) as f:
            self.label_map = json.load(f)
        class_num = len(self.label_map)
        self.net = model.PSPNet(n_classes=class_num, img_size=size)

        # デバイスを設定
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.net.to(self.device)

        # 高速化のため、ベンチマークモードをonにする
        torch.backends.cudnn.benchmark = True

    def load_weight(self):
        # 重みファイルの読み込み
        weight_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/weights.pth")
        self.net.load_state_dict(torch.load(weight_path, map_location=torch.device(self.device)))

    def predict(self, img):
        self.net.eval()
        img = img.convert("RGB")
        width, height = img.size
        dummy_annot = np.zeros(shape=(height, width), dtype=np.int32)
        img_transformed, _ = self.transformer('val', img, Image.fromarray(np.uint8(dummy_annot)))
        img_transformed  = img_transformed.unsqueeze(0)
        img_transformed = img_transformed.to(self.device)

        outputs = self.net(img_transformed)
        y = outputs[0].to('cpu')
        y = y[0].detach().numpy()
        annot = np.argmax(y, axis=0)
        return annot.tolist(), self.label_map