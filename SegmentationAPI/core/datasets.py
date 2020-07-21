import os
import json
import numpy as np
import cv2
from PIL import Image

import torch
import torch.utils.data as data

import utils.converter as converter

class SegmentationDataset(data.Dataset):
    """
    セマンティックセグメンテーションのDatasetクラス

    Attributes
    ----------
    list_file : string
        listファイル（画像ファイルのパスと対応するアノテーションファイルの組が記載されたファイル）のパス
    label_map : string
        label_mapファイルのパス
    transform : object
        前処理クラスのインスタンス
    phase : 'train' or 'val'
        学習か検証かを設定する
    """

    def __init__(self, list_file, label_map, transform, phase):
        self.transform = transform
        self.phase = phase
        self.images = []
        self.annotations = []


        # ラベルマップの読み込み
        with open(label_map) as f:
            self.label_map = json.load(f)
        
        root_path = os.path.dirname(list_file)
        data_list = open(list_file, "r")
        for line in data_list:
            img_path, annot_path = line.replace('\n', '').split(' ')
            self.images.append(os.path.join(root_path, img_path))
            self.annotations.append(os.path.join(root_path, annot_path))
    
    def __len__(self):
        '''画像の枚数を返す'''
        return len(self.images)
    
    def __getitem__(self, index):
        '''
        前処理をした画像のTensor形式のデータとアノテーション情報を取得
        '''
        # 1. 画像読み込み
        image_file_path = self.images[index]
        img = Image.open(image_file_path)   # [高さ][幅][色RGB]

        # 2. アノテーション画像読み込み
        anno_file_path = self.annotations[index]
        mask_img = Image.open(anno_file_path)
        anno_img = converter.mask2annot(mask_img, self.label_map)

        # 3. 前処理を実施
        img, anno_img = self.transform(self.phase, img, anno_img)

        # 4. anno_imgの型を変換（最終的にloss計算時にsoftmaxにかけるので、long型に変換）
        anno_img = anno_img.long()

        return img, anno_img