import subprocess
import os

# 获取当前路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 路径拼接
pipeline_path = os.path.join(current_dir, "pipeline.py")
save_path = os.path.join(current_dir, "save.py")

print("🚀 正在运行 pipeline.py ...")
pipeline_result = subprocess.run(["python", pipeline_path])

if pipeline_result.returncode != 0:
    print("❌ pipeline.py 运行失败，中止流程")
    exit(1)

print("✅ pipeline.py 执行完成\n")

print("🚀 正在运行 save.py ...")
save_result = subprocess.run(["python", save_path])

if save_result.returncode != 0:
    print("❌ save.py 运行失败")
    exit(1)

print("✅ 所有流程执行完成 🎉")
