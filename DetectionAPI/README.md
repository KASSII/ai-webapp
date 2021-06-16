# Detection API  
* 物体検出タスクのAPIサンプル  
* 本サンプルはVOCデータセットで学習した一般物体検出AIのAPI

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
| Name      | Type      | Description                                                     | 
| --------- | --------- | --------------------------------------------------------------- | 
| predict   | list      | 推論結果のリスト（クラス毎の推論結果が含まれる）                    | 
| ├ bbox    | list[int] | 検出した矩形の領域 [左上x座標, 左上y座標, 右下x座標, 右下y座標]     | 
| ├ label   | str       | 検出した物体のラベル                                              | 
| └prob     | float     | 信頼度                                                           | 
| label_map | list[str] | 各クラスのラベル名のリスト                                         | 

Responce example  
```
{
    "predict": [
        {
            "bbox": [10, 15, 100, 130],
            "label": "object1",
            "score": 99.5
        },
        {
            "bbox": [45, 5, 230, 65],
            "label": "object3",
            "score": 85.3
        }
    ],
    "label_map": [
        "object1",
        "object2",
        "object3"
    ]
}
```

#
## データ準備  
下記から学習済みモデルをダウンロードし、core/dataに保存する  
[https://drive.google.com/file/d/1m7S3D_ZoeIiulg4VMomdDSZh6lc91KOy/view?usp=sharing](https://drive.google.com/file/d/1m7S3D_ZoeIiulg4VMomdDSZh6lc91KOy/view?usp=sharing)

#  
## 動作確認  
1. 下記コマンドを実行してAPIを起動  
`> sh launch.sh`  

2. 別端末から下記スクリプトを実行、推論結果がコンソール上に表示されればOK  
`> cd test`  
`> python test.py`  

    実行結果  
    ```
    {"predict":[{"bbox":[81,58,493,259],"label":"aeroplane","score":99.79695677757263}],"label_map":["aeroplane","bicycle","bird","boat","bottle","bus","car","cat","chair","cow","diningtable","dog","horse","motorbike","person","pottedplant","sheep","sofa","train","tvmonitor"]}
    {"predict":[{"bbox":[55,80,484,341],"label":"horse","score":94.19537782669067},{"bbox":[31,93,131,341],"label":"person","score":78.40506434440613}],"label_map":["aeroplane","bicycle","bird","boat","bottle","bus","car","cat","chair","cow","diningtable","dog","horse","motorbike","person","pottedplant","sheep","sofa","train","tvmonitor"]}
    ```