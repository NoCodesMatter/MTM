from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 原有路由
    path('generate-music/', views.generate_music, name='generate_music'),  # 新增这条！
    path('upload-video/', views.upload_video, name='upload_video'),
]