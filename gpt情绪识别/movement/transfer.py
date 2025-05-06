import numpy as np
import pickle

# 绝对路径也可以改为你自己的
npy_path = "E:/AIGC/lmske_intermediate/features.npy"
pkl_path = "E:/AIGC/lmske_intermediate/features.pkl"

features = np.load(npy_path)
with open(pkl_path, "wb") as f:
    pickle.dump(features, f)

print("✅ 转换成功：features.pkl 已生成！")
