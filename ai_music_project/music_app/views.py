from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

import os
import tempfile
import json
import time
import shutil
import subprocess

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
        denoise = request.POST.get('denoise', 'false').lower() == 'true'
        
        # 获取音乐时长参数
        try:
            duration = int(request.POST.get('duration', '30'))
            if duration < 10:
                duration = 10
            elif duration > 60:
                duration = 60
        except ValueError:
            duration = 30
        
        # 检查是否上传了视频文件
        video_file = request.FILES.get('videoFile')
        video_path = None
        
        if video_file:
            # 创建临时文件存储上传的视频
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                for chunk in video_file.chunks():
                    tmp.write(chunk)
                video_path = tmp.name

        print(f"生成参数: 风格={genre}, 降噪={denoise}, 时长={duration}秒")
        response = connection.call_gpt_emotion(video_path, denoise=denoise, genre=genre, duration=duration)

        generated_music_path = response["music_path"]  # 这个是临时文件路径
        # 把生成的音乐文件复制到 MEDIA_ROOT/music/
        music_filename = os.path.basename(generated_music_path)
        music_save_path = os.path.join(settings.MEDIA_ROOT, 'music', music_filename)

        os.makedirs(os.path.dirname(music_save_path), exist_ok=True)
        shutil.copyfile(generated_music_path, music_save_path)

        # 构造前端可访问的 URL
        music_url = settings.MEDIA_URL + 'music/' + music_filename
        video_url = None
        
        # 如果是视频文件，也复制并提供URL
        if generated_music_path.endswith('.mp4'):
            video_url = music_url
            # 检查视频文件是否包含音频
            try:
                import ffmpeg
                video_probe = ffmpeg.probe(music_save_path)
                video_audio_streams = [stream for stream in video_probe['streams'] if stream['codec_type'] == 'audio']
                if not video_audio_streams:
                    print(f"⚠️ 警告: 保存的视频文件中没有音轨: {music_save_path}")
                else:
                    print(f"✅ 保存的视频包含 {len(video_audio_streams)} 个音轨")
                    for i, stream in enumerate(video_audio_streams):
                        print(f"  音轨 {i+1}: {stream.get('codec_name', 'unknown')}, {stream.get('channels', 'unknown')} 声道")
            except Exception as e:
                print(f"⚠️ 无法探测视频文件: {str(e)}")
        
        # 完整的URL路径（使用request.build_absolute_uri来获取完整路径）
        full_music_url = request.build_absolute_uri(music_url)
        full_video_url = request.build_absolute_uri(video_url) if video_url else None
        
        print("temp_music_url: ", generated_music_path)
        print("media_music_url: ", full_music_url)
        if full_video_url:
            print("media_video_url: ", full_video_url)

        # 构建响应数据
        result = {
            'success': True,
            'music_url': full_music_url,
            'generation_info': {
                'genre': genre,
                'complexity': complexity,
                'model': 'GPT Emotion Analysis',
                'duration': duration,  # 添加时长参数
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'video_url': full_video_url
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
        denoise = request.POST.get('denoise', 'false').lower() == 'true'
        
        # 获取音乐时长参数
        try:
            duration = int(request.POST.get('duration', '30'))
            if duration < 10:
                duration = 10
            elif duration > 60:
                duration = 60
        except ValueError:
            duration = 30
        
        # 检查是否上传了视频文件
        video_file = request.FILES.get('videoFile')
        video_path = None
        
        if video_file:
            # 创建临时文件存储上传的视频
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                for chunk in video_file.chunks():
                    tmp.write(chunk)
                video_path = tmp.name

        print(f"生成参数: 风格={genre}, 降噪={denoise}, 时长={duration}秒")
        response = connection.call_clip_emotion(video_path, denoise=denoise, genre=genre, duration=duration)

        generated_music_path = response["music_path"]  # 这个是临时文件路径
        # 把生成的音乐文件复制到 MEDIA_ROOT/music/
        music_filename = os.path.basename(generated_music_path)
        music_save_path = os.path.join(settings.MEDIA_ROOT, 'music', music_filename)

        os.makedirs(os.path.dirname(music_save_path), exist_ok=True)
        shutil.copyfile(generated_music_path, music_save_path)

        # 构造前端可访问的 URL
        music_url = settings.MEDIA_URL + 'music/' + music_filename
        video_url = None
        
        # 如果是视频文件，也复制并提供URL
        if generated_music_path.endswith('.mp4'):
            video_url = music_url
            # 检查视频文件是否包含音频
            try:
                import ffmpeg
                video_probe = ffmpeg.probe(music_save_path)
                video_audio_streams = [stream for stream in video_probe['streams'] if stream['codec_type'] == 'audio']
                if not video_audio_streams:
                    print(f"⚠️ 警告: 保存的视频文件中没有音轨: {music_save_path}")
                else:
                    print(f"✅ 保存的视频包含 {len(video_audio_streams)} 个音轨")
                    for i, stream in enumerate(video_audio_streams):
                        print(f"  音轨 {i+1}: {stream.get('codec_name', 'unknown')}, {stream.get('channels', 'unknown')} 声道")
            except Exception as e:
                print(f"⚠️ 无法探测视频文件: {str(e)}")
        
        # 完整的URL路径（使用request.build_absolute_uri来获取完整路径）
        full_music_url = request.build_absolute_uri(music_url)
        full_video_url = request.build_absolute_uri(video_url) if video_url else None
        
        print("temp_music_url: ", generated_music_path)
        print("media_music_url: ", full_music_url)
        if full_video_url:
            print("media_video_url: ", full_video_url)

        # 构建响应数据
        result = {
            'success': True,
            'music_url': full_music_url,
            'generation_info': {
                'genre': genre,
                'complexity': complexity,
                'model': 'Local English Model',
                'duration': duration,  # 添加时长参数
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'video_url': full_video_url
            }
        }
        
        # 如果是AJAX请求，返回JSON响应
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(result)
        
        # 对于普通表单提交，渲染结果页面
        return render(request, 'music_app/generated_music.html', {'result': result})
    
    # 如果不是POST请求，重定向到主页
    return render(request, 'music_app/music_generator.html')
    return render(request, 'music_app/music_generator.html')