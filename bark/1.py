from bark import generate_audio, preload_models
import torchaudio
import torch

# ✅ 预加载 Bark 模型（首次运行会自动下载）
preload_models()

# ✅ Bark 默认采样率
SAMPLE_RATE = 24000

# ✅ 输入文本
text = "[singing]  Late at night, I think of you, wondering if you miss me too.In this city full of lights, you're the only one that feels so right."

# ✅ 生成音频，选择一个温柔女声的 prompt（也可试试 'v2/en_speaker_4' 男声）
audio_array = generate_audio(text)

# ✅ 保存为 wav 文件
torchaudio.save("bark_output.wav", torch.from_numpy(audio_array).unsqueeze(0), SAMPLE_RATE)

print("✅ 音频生成完成，已保存为 bark_output.wav")
