from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

import os
import tempfile
import json
import time
import shutil

import connection

def index(request):
    """主页视图，渲染音乐生成界面"""
    return render(request, 'music_app/music_generator.html')

def upload_video(request):
    """处理视频上传请求"""
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        
        # 创建临时文件存储上传的视频
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            for chunk in video_file.chunks():
                tmp.write(chunk)
            video_path = tmp.name
        
        # 返回成功响应
        return JsonResponse({
            'success': True,
            'message': 'Video uploaded successfully',
            'temp_path': os.path.basename(video_path)
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    }, status=400)

def gpt_generate_music(request):
    """使用GPT模型生成音乐"""
    if request.method == 'POST':
        # 获取表单数据
        genre = request.POST.get('genre', 'electronic')
        complexity = request.POST.get('complexity', 'moderate')
        
        # 检查是否上传了视频文件
        video_file = request.FILES.get('videoFile')
        video_path = None
        
        if video_file:
            # 创建临时文件存储上传的视频
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                for chunk in video_file.chunks():
                    tmp.write(chunk)
                video_path = tmp.name

        response = connection.call_gpt_emotion(video_path)

        generated_music_path = response["music_path"]  # 这个是临时文件路径
        # 把生成的音乐文件复制到 MEDIA_ROOT/music/
        music_filename = os.path.basename(generated_music_path)
        music_save_path = os.path.join(settings.MEDIA_ROOT, 'music', music_filename)

        os.makedirs(os.path.dirname(music_save_path), exist_ok=True)
        shutil.copyfile(generated_music_path, music_save_path)

        # 构造前端可访问的 URL
        music_url = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'music/' + music_filename

        print("temp_music_url: ", generated_music_path)
        print("media_music_url: ", music_url)
        
        # 构建响应数据
        result = {
            'success': True,
            'music_url': music_url,
            'generation_info': {
                'genre': genre,
                'complexity': complexity,
                'model': 'Local English Model',
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        # 如果是AJAX请求，返回JSON响应
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(result)
        
        # 对于普通表单提交，渲染结果页面
        return render(request, 'music_app/generated_music.html', {'result': result})
    
    # 如果不是POST请求，重定向到主页
    return render(request, 'music_app/music_generator.html')

def local_model_generate_music(request):
    """使用本地CLIP大模型生成音乐"""
    if request.method == 'POST':
        # 获取表单数据
        genre = request.POST.get('genre', 'electronic')
        complexity = request.POST.get('complexity', 'moderate')
        
        # 检查是否上传了视频文件
        video_file = request.FILES.get('videoFile')
        video_path = None
        
        if video_file:
            # 创建临时文件存储上传的视频
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                for chunk in video_file.chunks():
                    tmp.write(chunk)
                video_path = tmp.name


        response = connection.call_clip_emotion(video_path)

        generated_music_path = response["music_path"]  # 这个是临时文件路径
        # 把生成的音乐文件复制到 MEDIA_ROOT/music/
        music_filename = os.path.basename(generated_music_path)
        music_save_path = os.path.join(settings.MEDIA_ROOT, 'music', music_filename)

        os.makedirs(os.path.dirname(music_save_path), exist_ok=True)
        shutil.copyfile(generated_music_path, music_save_path)

        # 构造前端可访问的 URL
        music_url = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'music/' + music_filename

        print("temp_music_url: ", generated_music_path)
        print("media_music_url: ", music_url)

        # 构建响应数据
        result = {
            'success': True,
            'music_url': music_url,
            'generation_info': {
                'genre': genre,
                'complexity': complexity,
                'model': 'Local English Model',
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        # 如果是AJAX请求，返回JSON响应
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(result)
        
        # 对于普通表单提交，渲染结果页面
        return render(request, 'music_app/generated_music.html', {'result': result})
    
    # 如果不是POST请求，重定向到主页
    return render(request, 'music_app/music_generator.html')