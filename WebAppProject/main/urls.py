from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/', views.project_overview, name='project_overview'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('dataset/<int:dataset_id>/', views.dataset_detail, name='dataset_detail'),
    path('train_log/<int:train_log_id>/', views.train_log_detail, name='train_log_detail'),
    path('evaluate/<int:train_log_id>/', views.evaluate, name='evaluate'),
    path('upload_test/', views.upload_test, name='upload_test'),
]