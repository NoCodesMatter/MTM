from django.shortcuts import render
from django.http import JsonResponse
import os
import tempfile
import json
import time

def index(request):
    """主页视图，渲染音乐生成界面"""
    return render(request, 'music_app/music_generator.html')

def generate_music(request):
    """处理音乐生成请求"""
    if request.method == 'POST':
        # 获取表单数据
        genre = request.POST.get('genre', 'electronic')
        length = int(request.POST.get('length', 60))
        tempo = int(request.POST.get('tempo', 120))
        complexity = request.POST.get('complexity', 'moderate')
        include_vocals = request.POST.get('includeVocals', 'off') == 'on'
        
        # 检查是否上传了视频文件
        video_file = request.FILES.get('videoFile')
        video_path = None
        
        if video_file:
            # 创建临时文件存储上传的视频
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                for chunk in video_file.chunks():
                    tmp.write(chunk)
                video_path = tmp.name
        
        # 在真实应用中，这里会调用AI模型生成音乐
        # 这里我们模拟一个处理过程
        time.sleep(3)  # 模拟处理时间
        
        # 使用示例音乐文件URL（实际项目中应替换为生成的音乐文件的路径）
        demo_music_url = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
        
        # 构建响应数据
        result = {
            'success': True,
            'music_url': demo_music_url,  # 使用示例音乐URL
            'generation_info': {
                'genre': genre,
                'length': length,
                'tempo': tempo,
                'complexity': complexity,
                'include_vocals': include_vocals,
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