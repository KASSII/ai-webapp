from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Project, Dataset

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
        raise Http404("Question does not exist")
    
    # Get relevant datasets
    dataset_list = Dataset.objects.filter(project=project)
    context = {"dataset_list": dataset_list}
    return render(request, 'main/project_detail.html', context)

@csrf_exempt
def upload_test(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'main/upload_test.html', context)
    elif request.method == 'POST':
        import pdb;pdb.set_trace()