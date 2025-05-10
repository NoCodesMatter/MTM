import os
import pickle
import sys
import argparse

# 设置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
extraction_dir = os.path.abspath(os.path.join(current_dir, "../Keyframe-Extraction-for-video-summarization-main/src/extraction"))
sys.path.append(extraction_dir)
from save_keyframe import save_frames_by_index_memory_cached

# ---------- 解析命令行参数 ----------
parser = argparse.ArgumentParser(description="从视频中保存关键帧图像")
parser.add_argument("video", nargs="?", default="happy.mp4", help="视频文件路径（可选）")
args = parser.parse_args()

# 构建路径
video_path = os.path.abspath(os.path.join(current_dir, args.video))
video_name = os.path.splitext(os.path.basename(video_path))[0]  # 获取不带扩展名的视频文件名
keyframe_pkl_path = os.path.join(current_dir, "lmske_intermediate", "keyframe_indices.pkl")
frames_list_path = os.path.join(current_dir, "lmske_intermediate", "frames_list.pkl")
output_folder = os.path.join(current_dir, "keyframes_output", video_name)  # 新建子文件夹

def main():
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在：{video_path}")
        return
    if not os.path.exists(keyframe_pkl_path):
        print(f"❌ 关键帧索引文件不存在：{keyframe_pkl_path}")
        return

    with open(keyframe_pkl_path, "rb") as f:
        keyframe_indexes = pickle.load(f)
    print(f"🔢 加载关键帧索引，共 {len(keyframe_indexes)} 项")

    save_frames_by_index_memory_cached(
        keyframe_indexes=keyframe_indexes,
        video_path=video_path,
        folder_path=output_folder,
        frames_list_path=frames_list_path
    )

if __name__ == "__main__":
    main()
