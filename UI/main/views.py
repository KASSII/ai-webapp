import json
import urllib.request
from PIL import Image, ImageDraw
from io import BytesIO
import base64
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Project
from .models import TaskType

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def project_overview(request):
    project_list = Project.objects.all()
    context = {"project_list": project_list}
    return render(request, 'main/project_overview.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    task_type = [e.name for e in TaskType][project.task_type]
    if request.method == "GET":
        context = {"project": project, "task_type": task_type}
        return render(request, 'main/project_detail.html', context)
    elif request.method == "POST":
        # APIへ送信するデータの作成
        encode_image = request.POST["encode_image"]
        obj = {
            "encode_image": encode_image
        }
        json_data = json.dumps(obj).encode("utf-8")

        # APIへ送信
        url = project.api_url
        method = "POST"
        headers = {"Content-Type" : "application/json"}
        api_request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(api_request) as api_response:
            api_response = api_response.read().decode("utf-8")
        predict = json.loads(api_response)["predict"]
        
        # task_typeごとにHTMLへ返すデータを推論結果から作成
        response = {}
        if task_type == "classification":
            # 推定確率順にソート
            predict.sort(key=lambda x: x['prob'], reverse=True)
            response = {
                "predict": predict
            }
        elif task_type == "detection":
            # 入力画像をデコード
            input_image = Image.open(BytesIO(base64.b64decode(encode_image.split(",")[-1])))
            # 描画用の画像をコピー
            draw_image = input_image.copy()
            draw = ImageDraw.Draw(draw_image)

            response_predict = []
            for predict_elem in predict:
                bbox = predict_elem["bbox"]
                label = predict_elem["label"]
                score = predict_elem["score"]
                # 対応するトリミング画像を作成
                trim_img = input_image.crop(tuple(bbox))
                buffered = BytesIO()
                trim_img.save(buffered, format="JPEG")
                encode_trim_img = base64.b64encode(buffered.getvalue()).decode('utf-8')

                response_predict.append({
                    "label": label,
                    "score": score,
                    "trim_img": encode_trim_img
                })

                # 元画像に矩形を描画した画像を作成
                draw.rectangle(tuple(bbox), outline=(255, 0, 0))
            
            # 描画した画像をエンコード
            buffered = BytesIO()
            draw_image.save(buffered, format="JPEG")
            encode_draw_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            response = {
                "predict": response_predict,
                "image": encode_draw_image
            }
        
        return HttpResponse(json.dumps(response), content_type="text/javascript")


