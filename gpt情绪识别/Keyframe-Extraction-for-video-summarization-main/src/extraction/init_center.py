import numpy as np


# def kmeans_init(data):
#     print("In the process of initialising the center")
#     n = len(data)
#     # calculate sqrt(n)
#     sqrt_n = int(np.sqrt(n))
#     centers = []
#     label = []

#     # pick init_center
#     while len(centers) < sqrt_n:

#         sse_min = float('inf')
#         for i in range(n):
#             center = centers.copy()
#             if np.any(data[i] != centers):
#                 center.append(data[i])
#                 center = np.array(center)
#                 # print(center)
#                 sse = 0.0

#                 # Cluster operation
#                 cluster_labels = np.zeros(len(data)).astype(int)
#                 for k in range(len(data)):
#                     distances = [np.sqrt(np.sum((data[k] - cen) ** 2)) for cen in center]
#                     nearest_cluster = np.argmin(distances)
#                     cluster_labels[k] = nearest_cluster

#                 # Based on the results of the cluster operation,calculate sse
#                 for j in range(len(center)):
#                     # Get the data points of the jth cluster
#                     cluster_points = []
#                     for l in range(len(cluster_labels)):
#                         if cluster_labels[l] == j:
#                             cluster_points.append(data[l])
#                     singe_sse = 0.0
#                     for point in cluster_points:
#                         squared_errors = np.linalg.norm(point - center[j])
#                         singe_sse += squared_errors
#                     sse += singe_sse

#                 if sse < sse_min:
#                     sse_min = sse
#                     join_center = data[i]
#                     label = cluster_labels.copy()

#         centers.append(join_center)

#     return np.array(label), np.array(centers)
import numpy as np

def kmeans_init(data):
    print("🧠 In the process of initialising the center")
    n = len(data)
    sqrt_n = int(np.sqrt(n))
    sqrt_n = max(1, sqrt_n)  # 至少聚1类
    centers = []
    label = []

    max_attempts = 30  # ✅ 最多尝试30轮避免死循环
    attempt_count = 0

    while len(centers) < sqrt_n:
        attempt_count += 1
        print(f"🔄 尝试第 {attempt_count} 次 | 当前中心数量：{len(centers)}/{sqrt_n}")

        if attempt_count > max_attempts:
            print("🚨 超过最大尝试次数，强制退出初始化")
            break

        sse_min = float('inf')
        join_center = None

        for i in range(n):
            center = centers.copy()

            if len(center) == 0:
                center.append(data[i])
            else:
                if np.any([np.array_equal(data[i], c) for c in center]):
                    continue
                center.append(data[i])

            center = np.array(center)
            sse = 0.0

            cluster_labels = np.zeros(len(data), dtype=int)
            for k in range(len(data)):
                distances = [np.linalg.norm(data[k] - cen) for cen in center]
                nearest_cluster = np.argmin(distances)
                cluster_labels[k] = nearest_cluster

            for j in range(len(center)):
                cluster_points = [data[l] for l in range(len(cluster_labels)) if cluster_labels[l] == j]
                singe_sse = sum(np.linalg.norm(point - center[j]) for point in cluster_points)
                sse += singe_sse

            if sse < sse_min:
                sse_min = sse
                join_center = data[i]
                label = cluster_labels.copy()

        if join_center is None:
            print("⚠️ 未找到最优中心，随机选择一个中心点")
            join_center = data[np.random.randint(0, n)]

        centers.append(join_center)

    return np.array(label), np.array(centers)
