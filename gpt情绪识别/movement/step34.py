import sys
import os

# ---------- 添加 extraction 文件夹到模块搜索路径 ----------
current_dir = os.path.dirname(os.path.abspath(__file__))
extraction_dir = os.path.abspath(os.path.join(current_dir, "../Keyframe-Extraction-for-video-summarization-main/src/extraction"))
sys.path.append(extraction_dir)

# ✅ 正确导入函数：从 Keyframe_extraction.py 文件中导入
from Keyframe_extraction import scen_keyframe_extraction

# ---------- 参数配置 ----------
scenes_path = os.path.join(current_dir, "test.mp4.scenes.txt")
features_path = os.path.join(current_dir, "../lmske_intermediate/features.pkl")
video_path = os.path.join(current_dir, "test.mp4")
save_path = os.path.join(current_dir, "../lmske_intermediate/keyframe_indices.pkl")
folder_path = os.path.join(current_dir, "../keyframes_output")

os.makedirs(folder_path, exist_ok=True)

# ---------- 执行 ----------
print("🚀 开始执行关键帧提取...")
scen_keyframe_extraction(
    scenes_path=scenes_path,
    features_path=features_path,
    video_path=video_path,
    save_path=save_path,
    folder_path=folder_path
)
print("✅ 提取完成！关键帧图像已保存到:", folder_path)
