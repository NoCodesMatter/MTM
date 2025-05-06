from bark import SAMPLE_RATE, generate_audio
from bark.generation import preload_models
import scipy.io.wavfile as wavfile
import numpy as np
# 预加载模型（第一次运行会自动下载）
print("🔁 正在加载 Bark 模型（仅首次下载会较慢）...")
preload_models()
SAMPLE_RATE = 24000

# 文本输入（你可以换成中文试试）
text_prompt = """
[singing] Late at night, I think of you, wondering if you miss me too.
[singing] In this city full of lights, you're the only one that feels so right.
[singing] The silence echoes when you're away.
[singing] But your voice brings peace to my day.
"""
segments = [line.strip() for line in text_prompt.strip().split('\n') if line.strip()]
final_audio = []
# 生成音频
print("🎧 正在生成音频...")
for i, segment in enumerate(segments):
    print(f"🎤 正在生成第 {i+1} 段语音：{segment}")
    audio_array = generate_audio(segment)
    final_audio.append(audio_array)
combined_audio = np.concatenate(final_audio)

# 💾 保存为 WAV 文件
output_path = "output.wav"
wavfile.write(output_path, SAMPLE_RATE, combined_audio)
print(f"✅ 生成完成！输出保存为：{output_path}")
