from bark import SAMPLE_RATE, generate_audio
from bark.generation import preload_models
import scipy.io.wavfile as wavfile

# 预加载模型（第一次运行会自动下载）
print("🔁 正在加载 Bark 模型（仅首次下载会较慢）...")
preload_models()

# 文本输入（你可以换成中文试试）
text_prompt = "La la la la la~ I love singing~ [laughs] Let's go to the park~"

# 生成音频
print("🎧 正在生成音频...")
audio_array = generate_audio(text_prompt)

# 保存为 WAV 文件
output_path = "output.wav"
wavfile.write(output_path, SAMPLE_RATE, audio_array)
print(f"✅ 音频生成完毕，保存为 {output_path}")
