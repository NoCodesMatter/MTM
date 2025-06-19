import os
import subprocess
import shlex
import ffmpeg
os.environ["PATH"] += os.pathsep + r"E:\tools\ffmpeg\bin"

# 后台接口
# ===== 调用gpt获得情感分析 =====
def call_gpt_emotion(video_path, denoise=False, genre="electronic"):
    current_path = os.path.dirname(os.path.abspath(__file__))

    # 获取当前项目主文件夹的路径
    project_root = os.path.dirname(current_path)

    # 如果需要降噪，先处理视频
    if denoise:
        video_path = denoise_video(video_path)
        print(f"🔊 使用降噪后的视频: {video_path}")

    # 转到gpt情绪识别文件夹，进行关键帧提取
    target_script = os.path.join(project_root, "Gpt_Emotion_Recognition")

    pipeline_path = os.path.join(target_script, "movement", "pipeline.py")
    save_path = os.path.join(target_script, "movement", "save.py")
    gpt_path = os.path.join(target_script, "movement", "Callgpt.py")

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_path = os.path.join(target_script, "movement", "keyframes_output", video_name)

    # 调用pipeline.py
    print("🚀 正在运行 pipeline.py ...")
    pipeline_result = subprocess.run(["python", pipeline_path, video_path])
    
    if pipeline_result.returncode != 0:
        print("❌ pipeline.py 运行失败，中止流程")
        exit(1)
    
    print("✅ pipeline.py 执行完成\n")
    
    # 调用save.py
    print("🚀 正在运行 save.py ...")
    save_result = subprocess.run(["python", save_path, video_path])
    
    if save_result.returncode != 0:
        print("❌ save.py 运行失败")
        exit(1)
    
    print("✅ 所有流程执行完成 🎉")
    
    # 调用Callgpt.py
    print("🚀 正在运行 Callgpt.py ...")
    gpt_result = subprocess.run(["python", gpt_path, frame_path])
    
    if gpt_result.returncode != 0:
        print("❌ Callgpt.py 运行失败")
        exit(1)
    
    print("✅ GPT执行完成 🎉")

    # 调用test_musicgen
    gen_path = os.path.join(project_root, "audiocraft", "test_musicgen.py")
    text_path = os.path.join(frame_path, "gpt_emotion_analysis.txt")

    with open(text_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        description = lines[-1].strip()  # 去除末尾换行符
    
    # 将音乐风格添加到描述中
    if genre and genre != "electronic":
        description = f"{description} in {genre} style"
    
    print(f"🎵 使用描述: '{description}' 生成音乐")
    music_url = music_generate(gen_path, description, frame_path, video_name, video_path)
    return music_url


# 视频降噪功能
def denoise_video(video_path, output_path=None):
    """使用FFmpeg对视频进行降噪处理
    
    Args:
        video_path: 输入视频路径
        output_path: 输出路径，如果为None则生成临时文件
        
    Returns:
        处理后的视频路径
    """
    import tempfile
    if output_path is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            output_path = tmp.name
    
    video_name = os.path.basename(video_path)
    print(f"🔊 对视频 {video_name} 进行降噪处理...")
    
    try:
        # 使用高质量降噪滤镜 hqdn3d
        (
            ffmpeg
            .input(video_path)
            .filter('hqdn3d', 4, 3, 6, 4.5)  # 亮度、色度、时间滤波器强度
            .output(output_path, vcodec='libx264', acodec='aac')
            .run(overwrite_output=True, quiet=True)
        )
        print(f"✅ 视频降噪处理完成: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ 视频降噪处理失败: {str(e)}")
        return video_path  # 失败时返回原始视频

# ===== 调用clip情感分析 =====
def call_clip_emotion(video_path, denoise=False, genre="electronic"):
    current_path = os.path.dirname(os.path.abspath(__file__))

    # 获取当前项目主文件夹的路径
    project_root = os.path.dirname(current_path)

    # 如果需要降噪，先处理视频
    if denoise:
        video_path = denoise_video(video_path)
        print(f"🔊 使用降噪后的视频: {video_path}")

    # 转到clip情绪识别文件夹
    clip_path = os.path.join(project_root, "ClIP_project", "emotion_detect.py")
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    print("🚀 正在运行 emotion_detect.py ...")
    clip_result = subprocess.run(["python", clip_path, video_path, video_name])
    print(clip_path)

    if clip_result.returncode != 0:
        print("❌ emotion_detect.py 运行失败")
        exit(1)

    print("✅ 所有流程执行完成 🎉")

    text_path = os.path.join(project_root, "ClIP_project", "analysis_output", video_name, "clip_emotion_analysis.txt")
    output_path = os.path.join(project_root, "ClIP_project", "analysis_output", video_name)
    gen_path = os.path.join(project_root, "audiocraft", "test_musicgen.py")

    # 读取情绪描述，调用generate
    with open(text_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        description = lines[-1].strip()  # 去除末尾换行符
    
    # 将音乐风格添加到描述中
    if genre and genre != "electronic":
        description = f"{description} in {genre} style"
    
    print(f"🎵 使用描述: '{description}' 生成音乐")
    music_url = music_generate(gen_path, description, output_path, video_name, video_path)
    return music_url


# 调用music_generate出音乐
def music_generate(gen_path, description, output_path, video_name, video_path):
    print("🚀 正在运行 test_musicgen.py ...")
    command = ["python", gen_path, description, output_path, video_name]
    print("💻 CMD:", " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)

    print("📤 STDOUT:\n", result.stdout)
    print("⚠️ STDERR:\n", result.stderr)

    if result.returncode != 0:
        print("❌ test_musicgen.py 运行失败")
        raise RuntimeError("test_musicgen.py 运行失败")

    print("✅ 所有流程执行完成 🎉")

    # 提取路径并返回
    music_path = os.path.join(output_path, video_name + ".wav")

    # 调用音频和视频合成
    final_path = combine_music_video(video_path, video_name, music_path, output_path)

    return {"status": "success", "music_path": final_path}


def combine_music_video(video_path, video_name, music_path, output_path):
    """合并视频和音频生成最终的视频文件
    
    Args:
        video_path: 原始视频路径
        video_name: 视频名称（不含扩展名）
        music_path: 生成的音乐路径
        output_path: 输出目录
        
    Returns:
        生成的视频文件路径
    """
    final_path = os.path.join(output_path, video_name + ".mp4")
    print("final_path: ", final_path)
    print("video_path: ", video_path)
    print("music_path: ", music_path)
    
    # 检查输入文件存在
    if not os.path.exists(video_path):
        print(f"❌ 错误: 视频文件不存在: {video_path}")
        return music_path
    
    if not os.path.exists(music_path):
        print(f"❌ 错误: 音频文件不存在: {music_path}")
        return video_path

    try:        # 先检查音频文件有效性
        try:
            audio_probe = ffmpeg.probe(music_path)
            audio_streams = [stream for stream in audio_probe['streams'] if stream['codec_type'] == 'audio']
            if not audio_streams:
                print(f"⚠️ 警告: 音频文件中没有音轨: {music_path}")
            else:
                print(f"✅ 音频文件有效: {len(audio_streams)} 个音轨")
                for i, stream in enumerate(audio_streams):
                    print(f"  音轨 {i+1}: {stream.get('codec_name', 'unknown')}, {stream.get('channels', 'unknown')} 声道")
        except Exception as e:
            print(f"⚠️ 无法探测音频文件: {str(e)}")
            
        # 使用直接的命令行调用，而不是ffmpeg-python API
        cmd = [
            "ffmpeg",
            "-i", video_path,   # 视频输入
            "-i", music_path,   # 音频输入
            "-c:v", "copy",     # 复制视频流
            "-c:a", "aac",      # 重新编码音频为AAC
            "-b:a", "192k",     # 音频比特率
            "-map", "0:v:0",    # 从第一个输入取视频
            "-map", "1:a:0",    # 从第二个输入取音频
            "-map_metadata", "-1",  # 去除元数据
            "-shortest",        # 使用最短的输入长度
            "-y",               # 覆盖输出
            final_path          # 输出文件
        ]
        
        # 打印命令用于调试
        print("FFmpeg command:", " ".join(cmd))
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 打印输出和错误
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"❌ FFmpeg 命令失败，返回码: {result.returncode}")
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        print("✅ 视频和音频合成成功: ", final_path)
        # 验证文件存在
        if os.path.exists(final_path):
            size_bytes = os.path.getsize(final_path)
            print(f"✅ 输出文件大小: {size_bytes / (1024*1024):.2f} MB")
            
            # 检查生成的文件是否包含音频
            try:
                output_probe = ffmpeg.probe(final_path)
                output_audio = [stream for stream in output_probe['streams'] if stream['codec_type'] == 'audio']
                if not output_audio:
                    print(f"⚠️ 警告: 生成的视频文件中没有音轨!")
                else:
                    print(f"✅ 生成的视频包含 {len(output_audio)} 个音轨")
            except Exception as e:
                print(f"⚠️ 无法探测输出文件: {str(e)}")
        else:
            print("⚠️ 警告: 输出文件不存在!")

        return final_path
    except Exception as e:
        print(f"❌ 视频音频合成失败: {str(e)}")
        # 失败时返回音频文件路径
        return music_path

# test case (文件名不能包含中文)
#call_gpt_emotion(r"E:\MTMusic\video_test\14.mp4")
#call_clip_emotion(r"E:\MTMusic\video_test\14.mp4")
def batch_run_emotion(video_dir, video_ids):
    for vid in video_ids:
        video_path = fr"{video_dir}\{vid}.mp4"
        print(f"▶ 正在处理视频：{video_path}")
        call_gpt_emotion(video_path)
        call_clip_emotion(video_path)

# 设置路径和编号范围
# video_dir = r"E:\MTMusic\video_test"
# video_ids = list(range(20, 25))  # 处理 16.mp4 到 20.mp4

#batch_run_emotion(video_dir, video_ids)
