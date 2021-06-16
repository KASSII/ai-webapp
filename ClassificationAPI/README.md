# Classification API  
* 分類タスクのAPIサンプル  
* 本サンプルはアリとハチの分類AIのAPI

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
| Name     | Type  | Description                                      | 
| -------- | ----- | ------------------------------------------------ | 
| predict  | list  | 推論結果のリスト（クラス毎の推論結果が含まれる）     | 
| ├ label  | str   | ラベル名                                          | 
| └prob    | float | 対応するラベルである確率（%）                       | 

Responce example  
```
{
    "predict": [
        {
            "label":"ant",
            "prob":90.2
        },
        {
            "label":"bee",
            "pprob":9.8
        }
    ]
}
```

#
## データ準備  
下記から学習済みモデルをダウンロードし、core/dataに保存する  
[https://drive.google.com/file/d/1ux4bZZl7mNIzQ37uqVtTOIhYGhJ2GntP/view?usp=sharing](https://drive.google.com/file/d/1ux4bZZl7mNIzQ37uqVtTOIhYGhJ2GntP/view?usp=sharing)

#  
## 動作確認  
1. 下記コマンドを実行してAPIを起動  
`> sh launch.sh`  

2. 別端末から下記スクリプトを実行、推論結果がコンソール上に表示されればOK  
`> cd test`  
`> python test.py`  

    実行結果  
    ```
    {"predict":[{"label":"ant","prob":99.96797180175781},{"label":"bee","prob":0.032031718641519547}]}  
    {"predict":[{"label":"ant","prob":0.0028223523404449224},{"label":"bee","prob":99.99717712402344}]}
    ```