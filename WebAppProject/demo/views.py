from django.shortcuts import get_object_or_404, render
from main.models import Project, TrainLog
from main.models import TaskType

# Create your views here.
def project_overview(request):
    project_list = Project.objects.filter(public=True)
    context = {"project_list": project_list}
    return render(request, 'demo/project_overview.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not project.public:
        raise Http404("Authentication error")
    
    train_log_list = TrainLog.objects.filter(project=project)          # Get relevant train log
    context = {"train_log_list": train_log_list}
    return render(request, 'demo/project_detail.html', context)

def inference(request, train_log_id):
    train_log = get_object_or_404(TrainLog, pk=train_log_id)
    if not train_log.project.public:
        raise Http404("Authentication error")

    if request.method == "GET":
        context = {}
        return render(request, 'demo/inference.html', context)