import os
import cv2
import pickle

def save_frames_by_index_memory_cached(keyframe_indexes, video_path, folder_path, frames_list_path=None):
    print(f"🔍 准备保存关键帧，视频路径：{video_path}")
    print(f"🔍 待保存关键帧数：{len(keyframe_indexes)}")
    print(f"🔍 保存目录是否存在：{os.path.exists(folder_path)}")

    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在：{video_path}")
        return

    # 加载帧编号映射（如果提供）
    real_frame_indices = None
    if frames_list_path and os.path.exists(frames_list_path):
        with open(frames_list_path, "rb") as f:
            real_frame_indices = pickle.load(f)
        print(f"📎 已加载帧编号映射文件，共 {len(real_frame_indices)} 项")

    keyframe_set = set(int(x) for x in keyframe_indexes)
    os.makedirs(folder_path, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ 无法打开视频文件：{video_path}")
        return

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"📊 视频帧总数：{total}")
    current_index = 0
    saved_count = 0
    frame_cache = {}

    print("📥 正在读取并缓存全部帧...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_cache[current_index] = frame
        current_index += 1

    cap.release()
    print(f"✅ 缓存完毕，共缓存 {len(frame_cache)} 帧，准备保存关键帧")

    for idx in sorted(keyframe_set):
        # 如果有帧索引映射，则转换为真实帧编号
        true_frame_idx = (
            real_frame_indices[idx] if real_frame_indices and idx < len(real_frame_indices) else idx
        )
        frame = frame_cache.get(true_frame_idx)

        if frame is None:
            print(f"❌ 帧 {true_frame_idx} 不存在")
            continue

        save_path = os.path.join(folder_path, f"{true_frame_idx}.jpg")
        success = cv2.imwrite(save_path, frame)
        if success:
            print(f"✅ 保存关键帧：{save_path}")
            saved_count += 1
        else:
            print(f"❌ 写入失败：{save_path}")

    print(f"🎉 共保存关键帧 {saved_count} 张")
