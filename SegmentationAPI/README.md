# Segmentation API  
* セグメンテーションタスクのAPIサンプル  
* 本サンプルはVOCデータセットで学習した一般物体セグメンテーションAIのAPI

#  
## API仕様  
### POST /predict  
* エンコードした画像を受け取り、推論結果を返す  

#### JSON body parameters  
| Name         | Type | Description                              | 
| ------------ | ---- | ---------------------------------------- | 
| encode_image | str  | base64で文字列にエンコードした画像データ    | 

JSON example  
```
{
    "encode_image": '/9j/4AAQSkZJRgA....
}
```

#### Response
| Name      | Type            | Description                                        | 
| --------- | --------------- | -------------------------------------------------- | 
| predict   | list[list[int]] | 各ピクセルに対応するラベルの値が入った推論結果画像      | 
| label_map | list            | ラベルごとの名前と色のリスト                          | 
| ├ name    | str             | ラベル名                                            | 
| └color    | list[int]       | ラベルごとに割り当てられた色（[R, G, B]）             | 

Responce example  
```
{
    "predict": [[0, 1, 0, ...],...[1, 0, 0, ...]],
    "label_map": [
        {
            "name":"object1",
            "color":[128,0,0]
        },
        {
            "name":"object2",
            "color":[0,255,128]
        },
        {
            "name":"object3",
            "color":[255,128,128]
        }
    ]
}
```

#
## データ準備  
下記から学習済みモデルをダウンロードし、core/dataに保存する  
[https://drive.google.com/file/d/1JbdPw6ywJqWvkZHVc_eo-Nw5LHSh1FPz/view?usp=sharing](https://drive.google.com/file/d/1JbdPw6ywJqWvkZHVc_eo-Nw5LHSh1FPz/view?usp=sharing)

#  
## 動作確認  
1. 下記コマンドを実行してAPIを起動  
`> sh launch.sh`  

2. 別端末から下記スクリプトを実行、推論結果がコンソール上に表示されてマスク画像が表示されればOK  
`> cd test`  
`> python test.py`  

    実行結果  
    ```
    (475, 475)
    [{'name': 'background', 'color': [0, 0, 0]}, {'name': 'aeroplane', 'color': [128, 0, 0]}, {'name': 'bicycle', 'color': [0, 128, 0]}, {'name': 'bird', 'color': [128, 128, 0]}, {'name': 'boat', 'color': [0, 0, 128]}, {'name': 'bottle', 'color': [128, 0, 128]}, {'name': 'bus', 'color': [0, 128, 128]}, {'name': 'car', 'color': [128, 128, 128]}, {'name': 'cat', 'color': [64, 0, 0]}, {'name': 'chair', 'color': [192, 0, 0]}, {'name': 'cow', 'color': [64, 128, 0]}, {'name': 'diningtable', 'color': [192, 128, 0]}, {'name': 'dog', 'color': [64, 0, 128]}, {'name': 'horse', 'color': [192, 0, 128]}, {'name': 'motorbike', 'color': [64, 128, 128]}, {'name': 'person', 'color': [192, 128, 128]}, {'name': 'pottedplant', 'color': [0, 64, 0]}, {'name': 'sheep', 'color': [128, 64, 0]}, {'name': 'sofa', 'color': [0, 192, 0]}, {'name': 'train', 'color': [128, 192, 0]}, {'name': 'tvmonitor', 'color': [0, 64, 128]}]
    (475, 475)
    [{'name': 'background', 'color': [0, 0, 0]}, {'name': 'aeroplane', 'color': [128, 0, 0]}, {'name': 'bicycle', 'color': [0, 128, 0]}, {'name': 'bird', 'color': [128, 128, 0]}, {'name': 'boat', 'color': [0, 0, 128]}, {'name': 'bottle', 'color': [128, 0, 128]}, {'name': 'bus', 'color': [0, 128, 128]}, {'name': 'car', 'color': [128, 128, 128]}, {'name': 'cat', 'color': [64, 0, 0]}, {'name': 'chair', 'color': [192, 0, 0]}, {'name': 'cow', 'color': [64, 128, 0]}, {'name': 'diningtable', 'color': [192, 128, 0]}, {'name': 'dog', 'color': [64, 0, 128]}, {'name': 'horse', 'color': [192, 0, 128]}, {'name': 'motorbike', 'color': [64, 128, 128]}, {'name': 'person', 'color': [192, 128, 128]}, {'name': 'pottedplant', 'color': [0, 64, 0]}, {'name': 'sheep', 'color': [128, 64, 0]}, {'name': 'sofa', 'color': [0, 192, 0]}, {'name': 'train', 'color': [128, 192, 0]}, {'name': 'tvmonitor', 'color': [0, 64, 128]}]
    ```