import os
import subprocess
import shlex
os.environ["PATH"] += os.pathsep + r"E:\tools\ffmpeg\bin"

# 后台接口
# ===== 调用gpt获得情感分析 =====
def call_gpt_emotion(video_path):
    current_path = os.path.dirname(os.path.abspath(__file__))

    # 获取当前项目主文件夹的路径
    project_root = os.path.dirname(current_path)

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

    music_url = music_generate(gen_path, description, frame_path, video_name)
    return music_url


# ===== 调用clip情感分析 =====
def call_clip_emotion(video_path):
    current_path = os.path.dirname(os.path.abspath(__file__))

    # 获取当前项目主文件夹的路径
    project_root = os.path.dirname(current_path)

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

    music_url = music_generate(gen_path, description, output_path, video_name)
    return music_url


# 调用music_generate出音乐
def music_generate(gen_path, description, output_path, video_name):
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
    return {"status": "success", "music_path": music_path}




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
