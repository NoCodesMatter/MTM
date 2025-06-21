import sys
import os
import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
model = MusicGen.get_pretrained('facebook/musicgen-large')  # 自动下载 medium 模型
# 不在这里设置时长，改为在实际生成前设置，以便使用命令行参数的值


# 测试用案例
# def test():
#     description = ["Joy: A fast-paced and thrilling electronic track with intense beats and energetic drops, reflecting the excitement and adrenaline of competitive gameplay."]
#     wav = model.generate(description)

#     audio_write("musicgen_medium.wav", wav[0].cpu(), model.sample_rate, format="wav")


# 实际调用函数
def generate(description, output_path, video_name, duration=30):
    # 设置音乐生成的时长参数
    print(f"[INFO] 设置模型生成时长参数: {duration}秒")
    model.set_generation_params(duration=duration)
    
    wav = model.generate(description)

    music_name = video_name
    music_path = os.path.join(output_path, music_name)

    audio_write(music_path, wav[0].cpu(), model.sample_rate, format="wav")

    print(f"[SUCCESS] 生成音乐路径: {music_path}, 时长: {duration}秒")
    return music_path


# 🧠 入口：从命令行获取视频名子文件夹
if __name__ == "__main__":
    # Windows终端可能有编码问题，确保正确处理
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    # 检查参数数量，允许4个或5个参数
    if len(sys.argv) < 4:
        print("[ERROR] 使用方法: python test_musicgen.py <描述文本> <输出路径> <视频名称> [音乐时长(秒)]")
        sys.exit(1)

    # 从命令行参数获取输入
    description = sys.argv[1]
    output_path = sys.argv[2]
    video_name = sys.argv[3]
    
    # 如果提供了时长参数，则使用指定的时长，否则使用默认值30秒
    duration = 30  # 默认时长
    if len(sys.argv) > 4:
        try:
            user_duration = int(sys.argv[4])
            # 限制时长在10-60秒范围内
            duration = max(10, min(60, user_duration))
            print(f"[INFO] 使用用户指定的时长: {duration}秒, 原始参数值: {sys.argv[4]}")
        except ValueError:
            print(f"[WARN] 无效的时长参数: {sys.argv[4]}，使用默认值30秒")
    
    print(f"生成描述: '{description}'")
    print(f"[INFO] 输出路径: {output_path}")
    print(f"[INFO] 视频名称: {video_name}")
    print(f"[INFO] 生成时长: {duration}秒")
    
    generate([description], output_path, video_name, duration)