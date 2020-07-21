import os
import json
import numpy as np
import cv2

import torch
import torch.utils.data as data

class DetectionDataset(data.Dataset):
    """
    一般物体認識のDatasetクラス

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
        self.bboxes = []
        self.labels = []

        # ラベルマップの読み込み
        with open(label_map) as f:
            self.label_map = json.load(f)
        
        root_path = os.path.dirname(list_file)
        data_list = open(list_file, "r")
        for line in data_list:
            img_path, annot_path = line.replace('\n', '').split(' ')
            self.images.append(os.path.join(root_path, img_path))
            with open(os.path.join(root_path, annot_path)) as f:
                annot = json.load(f)
            
            bboxes_for_img = []         # 1枚の画像に対するバウンディングボックス
            labels_for_image = []       # 1枚の画像に対するラベル
            for obj in annot["objects"]:
                bbox = obj["bbox"]
                label = self.label_map.index(obj["category"])
                bboxes_for_img.append(bbox)
                labels_for_image.append(label)
            self.bboxes.append(bboxes_for_img)
            self.labels.append(labels_for_image)

    def __len__(self):
        '''画像の枚数を返す'''
        return len(self.images)
    
    def __getitem__(self, index):
        '''
        前処理をした画像のTensor形式のデータとアノテーション情報を取得
        '''
        # index番目の画像をロード(transformで使用するオーグメンテーション関数がopencvで実装されているため、cv2で読み込む)
        img_path = self.images[index]
        img = cv2.imread(img_path)

        # index番目のアノテーション情報をロード
        bbox = np.asarray(self.bboxes[index])
        label = np.asarray(self.labels[index])

        # 前処理を実行
        img, bbox, label = self.transform(img, self.phase, bbox, label)

        # 色チャネルの順番がBGRになっているので、RGBに順番変更
        # さらに（高さ、幅、色チャネル）の順を（色チャネル、高さ、幅）に変換
        img = torch.from_numpy(img[:, :, (2, 1, 0)]).permute(2, 0, 1)

        # bboxとlabelをまとめてgtという変数にする
        gt = np.hstack((bbox, np.expand_dims(label, axis=1)))

        return img, gt


def od_collate_fn(batch):
    """
    アノテーションデータ（gt）のサイズが画像ごとに異なるため
    gtはリスト型で返すようなcollate_fn関数を作成
    """

    targets = []
    imgs = []
    for sample in batch:
        imgs.append(sample[0])  # sample[0] は画像img
        targets.append(torch.FloatTensor(sample[1]))  # sample[1] はアノテーションgt

    # imgsはミニバッチサイズのリストになっています
    # リストの要素はtorch.Size([3, 300, 300])です。
    # このリストをtorch.Size([batch_num, 3, 300, 300])のテンソルに変換します
    imgs = torch.stack(imgs, dim=0)

    # targetsはアノテーションデータの正解であるgtのリストです。
    # リストのサイズはミニバッチサイズです。
    # リストtargetsの要素は [n, 5] となっています。
    # nは画像ごとに異なり、画像内にある物体の数となります。
    # 5は [xmin, ymin, xmax, ymax, class_index] です

    return imgs, targets