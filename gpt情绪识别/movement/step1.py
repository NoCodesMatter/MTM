import os
import cv2
import numpy as np
from transnetv2 import TransNetV2

def detect_scenes(video_path, save_dir="scenes", visualize=False):
    # 创建模型
    model = TransNetV2()

    # 执行镜头预测
    print("[INFO] Running TransNetV2 on:", video_path)
    video_frames, single_frame_predictions, all_frame_predictions = model.predict_video(video_path)

    # 获取镜头段列表
    scene_list = model.predictions_to_scenes(single_frame_predictions)
    print(f"[INFO] Detected {len(scene_list)} scenes.")

    # 保存结果到文本文件
    scene_txt = video_path + ".scenes.txt"
    with open(scene_txt, "w") as f:
        for start, end in scene_list:
            f.write(f"{start} {end}\n")

    print(f"[INFO] Scene list saved to: {scene_txt}")

    # 可选：保存每个场景的起始帧图像
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        for i, (start, _) in enumerate(scene_list):
            frame = video_frames[start]
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            filename = os.path.join(save_dir, f"scene_{i:03d}_start.jpg")
            cv2.imwrite(filename, bgr_frame)
        print(f"[INFO] Saved scene start frames to: {save_dir}")

    # 可选：生成可视化图
    if visualize:
        vis_path = video_path + ".vis.png"
        model.visualize_predictions(video_frames, (single_frame_predictions, all_frame_predictions), vis_path)
        print(f"[INFO] Visualization saved to: {vis_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python step1.py /path/to/video.mp4")
    else:
        detect_scenes(sys.argv[1])
