
import os
from PIL import Image

def compress_images_in_folder(
    folder_path,
    output_folder=None,
    max_width=640,
    max_height=360,
    quality=80
):
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    count = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(folder_path, filename)

            # 设置输出路径（可同目录 or 新目录）
            if output_folder:
                output_path = os.path.join(output_folder, filename)
            else:
                output_path = input_path  # 直接覆盖原图

            try:
                with Image.open(input_path) as img:
                    # 转为 RGB（防止 PNG 带 alpha 报错）
                    img = img.convert("RGB")
                    img = img.resize((max_width, max_height))

                    # 保存为 JPEG 格式，压缩质量可调
                    img.save(output_path, "JPEG", quality=quality)
                    count += 1
            except Exception as e:
                print(f"❌ 压缩失败：{filename}，错误信息：{e}")

    print(f"\n✅ 压缩完成，共处理 {count} 张图片。")

# 示例用法
if __name__ == "__main__":
    folder = "movement\keyframes_output"  # 输入你的图片文件夹路径
    compress_images_in_folder(
        folder_path=folder,
        output_folder=None,      # None 表示覆盖原图；否则指定新目录
        max_width=480,
        max_height=270,
        quality=60               # 可调成 60～90，越低体积越小
    )
