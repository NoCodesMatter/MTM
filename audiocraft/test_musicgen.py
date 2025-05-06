import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
model = MusicGen.get_pretrained('facebook/musicgen-medium')  # 自动下载 medium 模型
model.set_generation_params(duration=30)  # 生成 30 秒音乐

descriptions = ["Joy: A fast-paced and thrilling electronic track with intense beats and energetic drops, reflecting the excitement and adrenaline of competitive gameplay."]
wav = model.generate(descriptions)

audio_write("musicgen_medium.wav", wav[0].cpu(), model.sample_rate, format="wav")