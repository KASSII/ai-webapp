import os
import json
import simplejson

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Project, Dataset
from .models import TaskType, ReadDbType
from AI_webApp.settings import DATASET_ROOT
from . import core

# Create your views here.
def index(request):
    context = {}
    return render(request, 'main/index.html', context)

@login_required
def project_overview(request):
    user = request.user
    project_list = Project.objects.filter(user=user)
    context = {"project_list": project_list}
    return render(request, 'main/project_overview.html', context)

@login_required
def project_detail(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if project.user.id != user.id:
        raise Http404("Authentication error")
    
    # Get relevant datasets
    dataset_list = Dataset.objects.filter(project=project)
    context = {"dataset_list": dataset_list}
    return render(request, 'main/project_detail.html', context)

@login_required
def dataset_detail(request, dataset_id):
    user = request.user
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    if dataset.project.user.id != user.id:
        raise Http404("Authentication error")

    dataset_path = os.path.join(DATASET_ROOT, '{}'.format(dataset_id))
    if request.method == "GET":
        with open(os.path.join(dataset_path, "meta_data.json")) as f:
            meta_data = json.load(f)
        data_num = meta_data["data_num"]
        context = {"dataset_name": dataset.name, "meta_data": meta_data}
        return render(request, 'main/dataset_detail.html', context)
    elif request.method == "POST":
        task_type = [e.name for e in TaskType][dataset.task_type - 1]
        start_idx = int(request.POST["start_idx"])
        request_data_num = int(request.POST["request_data_num"])
        loaded_data = core.read_dataset_controller.load_data(task_type, dataset_path, start_idx, request_data_num)
        # return json
        response = simplejson.dumps({'loaded_data':loaded_data}, use_decimal=True)
        return HttpResponse(response, content_type="text/javascript")

@csrf_exempt
def upload_test(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'main/upload_test.html', context)
    elif request.method == 'POST':
        import pdb;pdb.set_trace()