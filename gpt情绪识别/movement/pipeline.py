import os
import sys
import cv2
import torch
import pickle
import numpy as np

from tqdm import tqdm
from PIL import Image
import clip
from transnetv2 import TransNetV2

# ✅ 导入关键帧提取函数
current_dir = os.path.dirname(os.path.abspath(__file__))
extraction_dir = os.path.abspath(os.path.join(current_dir, "../Keyframe-Extraction-for-video-summarization-main/src/extraction"))
sys.path.append(extraction_dir)
# print("模块搜索路径：", extraction_dir)
from Keyframe_extraction import scen_keyframe_extraction
# from save_keyframe import save_frames_by_index_memory_cached

# ---------- 参数配置 ----------
# video_path = os.path.join(current_dir, "test.mp4")
video_path = os.path.abspath(os.path.join(current_dir, "../movement/fixed_test.mp4"))
print("🎯 正在使用视频路径：", video_path)
output_dir = os.path.join(current_dir, "lmske_intermediate")
scenes_path = os.path.join(output_dir, "scene_list.txt")
features_npy_path = os.path.join(output_dir, "features.npy")
features_pkl_path = os.path.join(output_dir, "features.pkl")  # 为兼容原逻辑
frames_list_path = os.path.join(output_dir, "frames_list.pkl")
keyframe_pkl_path = os.path.join(output_dir, "keyframe_indices.pkl")
keyframe_img_folder = os.path.join(current_dir, "keyframes_output")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(keyframe_img_folder, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"

# ---------- Step 1：镜头检测 ----------
def detect_scenes():
    print("🎬 Step 1: Running TransNetV2...")
    model = TransNetV2()
    video_frames, single_frame_predictions, _ = model.predict_video(video_path)
    scene_list = model.predictions_to_scenes(single_frame_predictions)

    with open(scenes_path, "w") as f:
        for start, end in scene_list:
            f.write(f"{start} {end}\n")

    print(f"✅ 镜头检测完成，共 {len(scene_list)} 段，已保存至 {scenes_path}")
    return scene_list

# ---------- Step 2：提取帧特征 ----------
def extract_clip_features():
    print("🧠 Step 2: 提取视频帧语义特征（CLIP）...")
    model, preprocess = clip.load("ViT-B/32", device=device)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    features = []
    frame_indices = []

    for i in tqdm(range(total_frames), desc="提取中"):
        ret, frame = cap.read()
        if not ret:
            break

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_pre = preprocess(img).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = model.encode_image(img_pre).cpu().numpy().squeeze()

        features.append(embedding)
        frame_indices.append(i)

    cap.release()

    np.save(features_npy_path, np.array(features))
    with open(frames_list_path, "wb") as f:
        pickle.dump(frame_indices, f)

    # 为兼容 Keyframe_extraction 原逻辑，存一份 .pkl 特征
    with open(features_pkl_path, "wb") as f:
        pickle.dump(features, f)

    print(f"✅ 特征提取完成，共 {len(features)} 帧")

# ---------- Step 3&4：提取关键帧 ----------
def run_keyframe_extraction():
    print("🧩 Step 3: 开始关键帧聚类提取...")
    scen_keyframe_extraction(
        scenes_path=scenes_path,
        features_path=features_pkl_path,
        video_path=video_path,
        save_path=keyframe_pkl_path,
        folder_path=keyframe_img_folder,
        frames_list_path="lmske_intermediate/frames_list.pkl"
    )
    # if os.path.exists(keyframe_img_folder) and os.listdir(keyframe_img_folder):
    #     print("✅ Step 4: 提取完成，关键帧保存在:", keyframe_img_folder)
    # else:
    #     print("⚠️ Step 4：没有保存任何关键帧，请检查提取逻辑或保存路径。")
    

# def save_keyframes_from_pkl(keyframe_pkl, frames_list_pkl, video_path, output_folder):
#     with open(keyframe_pkl, "rb") as f:
#         keyframe_indices = pickle.load(f)
#     print(f"🔢 加载关键帧编号，共 {len(keyframe_indices)} 张")
#     print("✔️ 关键帧索引示例：", keyframe_indices[:5])

#     save_frames_by_index_memory_cached(
#         keyframe_indexes=keyframe_indices,
#         video_path=video_path,
#         folder_path=output_folder,
#         frames_list_path=frames_list_pkl
#     )

# ---------- 执行流程 ----------
if __name__ == "__main__":
    if not os.path.exists(video_path):
        print(f"❌ 未找到视频：{video_path}")
        sys.exit()

    detect_scenes()
    extract_clip_features()
    run_keyframe_extraction()
    # save_keyframes_from_pkl(
    #     keyframe_pkl=keyframe_pkl_path,
    #     frames_list_pkl=frames_list_path,
    #     video_path=video_path,
    #     output_folder=keyframe_img_folder
    # )