import os
import numpy as np
from PIL import Image

import torch
import torch.utils.data as data

class ClassificationDataset(data.Dataset):
    """
    シングルラベル画像分類のDatasetクラス

    Attributes
    ----------
    list_file : string
        listファイル（画像ファイルのパスと対応するラベルの組が記載されたファイル）のパス
    transform : object
        前処理クラスのインスタンス
    phase : 'train' or 'val'
        学習か検証かを設定する。
    """
    def __init__(self, list_file, transform=None, phase='train'):
        self.transform = transform
        self.phase = phase
        self.images = []
        self.labels = []

        root_path = os.path.dirname(list_file)
        data_list = open(list_file, "r")
        for line in data_list:
            img_path, label = line.split(' ')
            self.images.append(os.path.join(root_path, img_path))
            self.labels.append(int(label))

    def __len__(self):
        '''画像の枚数を返す'''
        return len(self.images)
        
    def __getitem__(self, index):
        '''
        前処理をした画像のTensor形式のデータとラベルを取得
        '''
        # index番目の画像をロード
        img_path = self.images[index]
        img = Image.open(img_path)  # [高さ][幅][色RGB]

        # 画像の前処理を実施
        if self.transform is not None:
            img_transformed = self.transform(img, self.phase)  # torch.Size([3, 224, 224])
        else:
            img_transformed = np.asarray(img)
        
        # ラベルを取得
        label = self.labels[index]
        
        return img_transformed, label

