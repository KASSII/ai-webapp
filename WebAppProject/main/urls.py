from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/', views.overview_project, name='overview_project'),
    path('project/<int:project_id>/', views.detail_project, name='detail_project'),
    path('upload_test/', views.upload_test, name='upload_test'),
]