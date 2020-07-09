from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/', views.project_overview, name='project_overview'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('upload_test/', views.upload_test, name='upload_test'),
]