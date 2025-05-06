import pickle
import cv2
import numpy as np

from Kmeans_improvment import kmeans_silhouette
from save_keyframe import save_frames_by_index_memory_cached
from Redundancy import redundancy


def scen_keyframe_extraction(scenes_path, features_path, video_path, save_path, folder_path, frames_list_path=None):
    # Get lens segmentation data
    number_list = []
    with open(scenes_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line)
            numbers = line.strip().split(' ')
            print(numbers)
            number_list.extend([int(number) for number in numbers])

    # Read inference data from local
    with open(features_path, 'rb') as file:
        features = pickle.load(file)

    features = np.asarray(features)
    # print(len(features))

    # Clustering at each shot to obtain keyframe sequence numbers
    # keyframe_index = []
    # for i in range(0, len(number_list) - 1, 2):
    #     start = number_list[i]
    #     end = number_list[i + 1]
    #     # print(start, end)
    #     # sub_features = features[start:end]
    #     # best_labels, best_centers, k, index = kmeans_silhouette(sub_features)
    #     sub_features = features[start:end]
    #     if sub_features.ndim != 2 or sub_features.shape[0] < 2:
    #         print(f"⚠️  跳过空镜头段：start={start}, end={end}")
    #         continue
    #     best_labels, best_centers, k, index = kmeans_silhouette(sub_features)
    #     # print(index)
    #     final_index = [x + start for x in index]
    #     # final_index.sort()
    #     # print("clustering：" + str(keyframe_index))
    #     # print(start, end)
    #     final_index = redundancy(video_path, final_index, 0.94)
    #     # print(final_index)
    #     keyframe_index += final_index
    keyframe_index = []
    skipped = 0
    processed = 0

    for i in range(0, len(number_list) - 1, 2):
        start = number_list[i]
        end = number_list[i + 1]
        sub_features = features[start:end]

        if sub_features.ndim != 2 or sub_features.shape[0] < 2:
            print(f"⚠️  跳过无效镜头段：start={start}, end={end}，帧数不足 2（共 {sub_features.shape[0]} 帧）")
            skipped += 1
            continue

        # # ✅ 降采样并保留帧号映射
        # if sub_features.shape[0] > 300:
        #     print(f"⚠️  特征过多（{sub_features.shape[0]}），正在随机采样至 300 帧用于聚类")
        #     indices = np.random.choice(sub_features.shape[0], 300, replace=False)
        #     sampled_frame_ids = np.array(range(start, end))[indices]
        #     sub_features = sub_features[indices]
        # else:
        #     sampled_frame_ids = np.array(range(start, end))
        sampled_frame_ids = np.array(range(start, end))

        print(f"✅ 进入聚类：sub_features shape = {sub_features.shape}")

        try:
            best_labels, best_centers, k, index = kmeans_silhouette(sub_features)
        except Exception as e:
            print(f"❌ 聚类失败（{start}-{end}）：{e}")
            skipped += 1
            continue

        # ✅ 正确还原真实关键帧编号
        final_index = [sampled_frame_ids[x] for x in index]
        final_index = redundancy(video_path, final_index, 0.94)
        keyframe_index += final_index

        processed += 1
        print(f"✅ 提取关键帧数：{len(final_index)}")



    keyframe_index = [int(x) for x in keyframe_index]
    keyframe_index.sort()
    print("final_index：" + str(keyframe_index))

    # save keyframe
    # save_frames(keyframe_index, video_path, save_path, folder_path)
    # save_frames_by_index(keyframe_index, video_path, folder_path=folder_path)
    # save_frames_by_index_memory_cached(
    #     keyframe_index,  # ← 你的关键帧列表
    #     video_path,
    #     folder_path,
    #     frames_list_path=frames_list_path
    # )
    # 保存关键帧编号列表
    
    with open(save_path, "wb") as f:
        pickle.dump(keyframe_index, f)
    print(f"📁 已保存关键帧编号到：{save_path}")

    print(f"\n🎉 提取完毕：处理镜头段 {processed} 个，跳过 {skipped} 个")
    print(f"📦 共选出关键帧 {len(keyframe_index)} 张\n")



