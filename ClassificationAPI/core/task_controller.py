import os
import json
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import models

from . import transform

class TaskController():
    def __init__(self):
        # Transformerを定義
        size = 224
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)
        self.transformer = transform.DefaultTransform(size, mean, std)
    
        # ネットワークモデルの作成
        label_map_path = "core/data/label_map.json"
        with open(label_map_path) as f:
            self.label_map = json.load(f)
        class_num = len(self.label_map)

        self.net = models.vgg16()
        self.net.classifier[6] = nn.Linear(in_features=4096, out_features=class_num)

        # デバイスを設定
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.net.to(self.device)

        # 高速化のため、ベンチマークモードをonにする
        torch.backends.cudnn.benchmark = True

    def load_weight(self):
        # 重みファイルの読み込み
        weight_path = "core/data/weights.pth"
        self.net.load_state_dict(torch.load(weight_path, map_location=torch.device(self.device)))

    def predict(self, img):
        self.net.eval()
        img = img.convert("RGB")
        img_transformed = self.transformer(img, 'val')
        img_transformed  = img_transformed.unsqueeze(0)
        img_transformed = img_transformed.to(self.device)

        outputs = self.net(img_transformed)
        probs = F.softmax(outputs[0], dim=0).to('cpu')
        probs = probs.detach().numpy() * 100

        result = []
        for label, prob in zip(self.label_map, probs):
            result.append({"label": label, "prob": float(prob)})
        return result