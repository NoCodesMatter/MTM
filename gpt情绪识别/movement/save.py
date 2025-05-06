import os
import pickle
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
extraction_dir = os.path.abspath(os.path.join(current_dir, "../Keyframe-Extraction-for-video-summarization-main/src/extraction"))
sys.path.append(extraction_dir)
from save_keyframe import save_frames_by_index_memory_cached

# 配置路径（请根据实际情况修改）
video_path = "fixed_test.mp4"
keyframe_pkl_path = "lmske_intermediate/keyframe_indices.pkl"
frames_list_path = "lmske_intermediate/frames_list.pkl"
output_folder = "keyframes_output"

def main():
    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在：{video_path}")
        return
    if not os.path.exists(keyframe_pkl_path):
        print(f"❌ 关键帧索引文件不存在：{keyframe_pkl_path}")
        return

    # 加载关键帧索引
    with open(keyframe_pkl_path, "rb") as f:
        keyframe_indexes = pickle.load(f)
    print(f"🔢 加载关键帧索引，共 {len(keyframe_indexes)} 项")

    # 调用保存函数
    save_frames_by_index_memory_cached(
        keyframe_indexes=keyframe_indexes,
        video_path=video_path,
        folder_path=output_folder,
        frames_list_path=frames_list_path  # 你可以改成 None
    )

if __name__ == "__main__":
    main()
