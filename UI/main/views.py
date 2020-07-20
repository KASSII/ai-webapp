import json
import urllib.request
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
    if request.method == "GET":
        context = {"project": project}
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
            predict = api_response.read().decode("utf-8")
        predict = json.loads(predict)
        
        # task_typeごとにHTMLへ返すデータを推論結果から作成
        task_type = [e.name for e in TaskType][project.task_type]
        if task_type == "classification":
            # 推定確率順にソート
            predict = sorted(predict.items(), key=lambda x:x[1], reverse=True)
            response = {
                "predict": predict
            }
        
        return HttpResponse(json.dumps(response), content_type="text/javascript")


