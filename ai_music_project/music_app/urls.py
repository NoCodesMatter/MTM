from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 原有路由
    path('upload-video/', views.upload_video, name='upload_video'),
    path('gpt-generate-music/', views.gpt_generate_music, name='gpt_generate_music'),
    path('local-model-generate-music/', views.local_model_generate_music, name='local_model_generate_music'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)