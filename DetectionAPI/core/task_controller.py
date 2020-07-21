import os
import json
import numpy as np
import cv2

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import models

from . import transform
from . import model

class TaskController():
    def __init__(self):
        # 設定ファイルを読み込む
        cfg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/SSD300_config.json")
        with open(cfg_file) as f:
            ssd_cfg = json.load(f)
        
        # label_mapの読み込み
        label_map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/label_map.json")
        with open(label_map_path) as f:
            self.label_map = json.load(f)
        class_num = len(self.label_map)
        ssd_cfg["num_classes"] = class_num + 1  # 背景クラスを含めた合計クラス数

        # Transformerを定義
        mean = (104, 117, 123)
        self.transformer = transform.SSDTransform(ssd_cfg["input_size"], mean)
    
        # ネットワークモデルの作成
        self.net = model.SSD(phase="inference", cfg=ssd_cfg)

        # デバイスを設定
        self.device = "cpu"
        self.net.to(self.device)

        # 高速化のため、ベンチマークモードをonにする
        torch.backends.cudnn.benchmark = True

    def load_weight(self):
        # 重みファイルの読み込み
        weight_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/weights.pth")
        self.net.load_state_dict(torch.load(weight_path, map_location=torch.device('cpu')))

    def predict(self, img):
        self.net.eval()
        img = np.array(img, dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        height, width, _ = img.shape
        img_transformed, _, _ = self.transformer(img, 'val', np.zeros((1, 4)), np.zeros((1, 1)))     # アノテーションはダミーデータを入力
        img_transformed = torch.from_numpy(img_transformed[:, :, (2, 1, 0)]).permute(2, 0, 1)
        img_transformed = img_transformed.unsqueeze(0)     # 先頭にミニバッチの次元を追加
        img_transformed = img_transformed.to(self.device)
        
        outputs = self.net(img_transformed)
        outputs = outputs.cpu().detach().numpy()

        # 条件以上の値を抽出
        find_index = np.where(outputs[:, 0:, :, 0] >= 0.6)   # outputs[:, 0:, :, 0]はoutputsのconf情報のみを抽出している（[1, 21, 200]サイズ、つまり[minibatch, クラス、top]サイズ）
        outputs = outputs[find_index]

        result = []
        for i in range(len(find_index[1])):
            # 背景クラスは無視する
            if (find_index[1][i]) == 0:
                continue
            
            score = outputs[i][0]
            bbox = outputs[i][1:] * [width, height, width, height]
            label_index = find_index[1][i]-1        # 0を背景クラスにしているので1を引く
            label_name = self.label_map[label_index]

            result.append({
                "bbox": bbox.astype(np.int).tolist(),
                "label": label_name,
                "score": float(score) * 100
            })
        
        return result