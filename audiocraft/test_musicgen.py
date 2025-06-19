import sys
import os
import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
model = MusicGen.get_pretrained('facebook/musicgen-medium')  # 自动下载 medium 模型
model.set_generation_params(duration=30)  # 生成与视频时间相同的音乐


# 测试用案例
# def test():
#     description = ["Joy: A fast-paced and thrilling electronic track with intense beats and energetic drops, reflecting the excitement and adrenaline of competitive gameplay."]
#     wav = model.generate(description)

#     audio_write("musicgen_medium.wav", wav[0].cpu(), model.sample_rate, format="wav")


# 实际调用函数
def generate(description, output_path, video_name):
    wav = model.generate(description)

    music_name = video_name
    music_path = os.path.join(output_path, music_name)

    audio_write(music_path, wav[0].cpu(), model.sample_rate, format="wav")

    print(music_path)
    return music_path


# 🧠 入口：从命令行获取视频名子文件夹
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("未找到正确的描述")
        sys.exit(1)

    # 从命令行参数获取输入
    description = sys.argv[1]
    output_path = sys.argv[2]
    video_name = sys.argv[3]
    generate([description], output_path, video_name)