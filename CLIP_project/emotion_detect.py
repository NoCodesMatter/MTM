import torch
print("CUDA available:", torch.cuda.is_available())
print("Device count:", torch.cuda.device_count())
print("Current device:", torch.cuda.current_device() if torch.cuda.is_available() else "None")
# !nvidia-smi

import cv2
import torch
import clip
import numpy as np
from PIL import Image
from typing import List
import sys
import os

# 设备选择
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# 加载模型和预处理器
model, preprocess = clip.load("ViT-B/32", device=device)

model.float()

# 情绪提示词
emotion_labels = [
    # 喜 Joy
    "Joy: a vibrant scene with warm sunlight, blooming flowers, bright colors, and a peaceful landscape that evokes happiness.A dynamic and energetic scene full of movement, bright lights, fireworks, and visual excitement like a festival or concert",

    # 怒 Anger
    "Anger: a dramatic and chaotic environment with dark clouds, aggressive fire, broken structures, and intense tension in the atmosphere",

    # 哀 Sadness
    "Sadness: a lonely and desaturated scene of a rainy day, empty streets, or a quiet foggy forest that feels melancholic and heavy",

    # 害怕 Fear
    "Fear: a dark and eerie environment with shadows, fog, abandoned buildings, or looming shapes that create a strong sense of danger, suspense, or unease",

    "Excited: A fast-paced and thrilling electronic track with intense beats and energetic drops, reflecting the excitement and adrenaline of competitive gameplay."

    # 宁静 Inner Peace
    "Inner Peace: a calm and tranquil natural scene with soft sunlight, still water, open space, gentle hills or mountains, and a feeling of deep serenity"
]
emotion_list = ["Joy", "Anger", "Sadness", "Fear", "Excited", "Inner Peace"]
text_prompts = [f"a scene evoking {e}" for e in emotion_labels]
text_tokens = clip.tokenize(text_prompts).to(device)

def extract_frames(video_path: str, interval_sec: float = 1.0) -> List[Image.Image]:
    """
    每 interval_sec 截取一帧，返回 PIL 图像列表
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    frames = []

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frames.append(image_pil)
        frame_idx += 1

    cap.release()
    return frames


def predict_emotion_for_images(images: List[Image.Image], model, preprocess, text_features, device="cpu") -> np.ndarray:
    """
    对图像列表进行情绪识别，返回每帧情绪得分组成的数组 shape=[num_frames, num_emotions]
    """
    all_probs = []
    with torch.no_grad():
        for img in images:
            image_input = preprocess(img).unsqueeze(0).to(device)
            image_features = model.encode_image(image_input)
            logits_per_image = (image_features @ text_features.T).softmax(dim=-1)
            all_probs.append(logits_per_image.cpu().numpy()[0])
    return np.array(all_probs)


def analyze_video_emotion(video_path: str, video_name: str, model, preprocess, device="cpu") -> None:
    """
    主函数：输入视频路径，输出分析结果
    """
    print(f"⏳ 正在处理视频: {video_path}")
    # 1. 编码文本特征（只做一次）
    text_tokens = clip.tokenize(text_prompts).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)

    # 2. 提取帧
    frames = extract_frames(video_path, interval_sec=1.0)
    print(f"✅ 提取帧数: {len(frames)}")

    if not frames:
        print("⚠️ 未提取到帧，检查视频文件是否有效")
        return ''

    # 3. 图像预测
    all_probs = predict_emotion_for_images(frames, model, preprocess, text_features, device=device)

    # 4. 汇总分析
    avg_probs = all_probs.mean(axis=0)

    # 5. 输出
    print("\n📊 视频情绪分布：")
    for emotion, score in zip(emotion_labels, avg_probs):
        # 只打印第一个冒号前面的情感名称
        emotion_name = emotion.split(":")[0]
        print(f"{emotion_name:<15}: {score:.3f}")

    print("\n🌟 推测视频情感基调：", emotion_labels[np.argmax(avg_probs)].split(":")[0])

    target_emotion = emotion_labels[np.argmax(avg_probs)].split(":")[0]
    index = emotion_list.index(target_emotion)
    description = emotion_labels[index]     # 通过索引获取 emotion_labels 中的对应描述

    current_path = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_path, "analysis_output", video_name)  # 新建子文件夹
    os.makedirs(output_folder, exist_ok=True)  # 创建文件夹（如果不存在）
    output_path = os.path.join(current_path, "analysis_output", video_name, "clip_emotion_analysis.txt")
    with open(output_path, "w", ) as f:
        f.write(description)
        f.close()


# 🧠 入口：从命令行获取视频名子文件夹
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("未找到正确的音乐路径")
        sys.exit(1)

    # 从命令行参数获取输入
    music_path = sys.argv[1]
    video_name = sys.argv[2]

    analyze_video_emotion(music_path, video_name, model, preprocess, device=device)