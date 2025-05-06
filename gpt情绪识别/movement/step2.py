import os
import cv2
import torch
import pickle
import numpy as np
from tqdm import tqdm
from PIL import Image
import clip  # 使用英文版 OpenAI CLIP

# ---------- 配置 ----------
video_path = "./movement/test.mp4"                # ← 修改为你的视频路径
output_dir = "lmske_intermediate"            # ← 中间结果输出路径
device = "cuda" if torch.cuda.is_available() else "cpu"

# ---------- 初始化 ----------
os.makedirs(output_dir, exist_ok=True)
print("🚀 正在加载英文 CLIP 模型...")
model, preprocess = clip.load("ViT-B/32", device=device)

# ---------- 提取特征 ----------
def extract_clip_features(video_path):
    print("🧠 开始提取视频帧语义特征（英文 CLIP）...")
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    features = []
    frame_indices = []

    for i in tqdm(range(total_frames), desc="提取中"):
        ret, frame = cap.read()
        if not ret:
            break

        # 转换为 RGB 图像
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_pre = preprocess(img).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = model.encode_image(img_pre).cpu().numpy().squeeze()

        features.append(embedding)
        frame_indices.append(i)

    cap.release()

    # 保存结果
    np.save(os.path.join(output_dir, "features.npy"), np.array(features))
    with open(os.path.join(output_dir, "frames_list.pkl"), "wb") as f:
        pickle.dump(frame_indices, f)

    print(f"✅ 提取完成：{len(features)} 帧，结果保存在：{output_dir}/")

# ---------- 执行 ----------
if __name__ == "__main__":
    if not os.path.exists(video_path):
        print("❌ 视频路径不存在，请检查 video_path")
    else:
        extract_clip_features(video_path)
