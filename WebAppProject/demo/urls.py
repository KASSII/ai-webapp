from django.urls import path

from . import views

urlpatterns = [
    path('project/', views.project_overview, name='project_overview'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('inference/<int:train_log_id>/', views.inference, name='inference'),
]