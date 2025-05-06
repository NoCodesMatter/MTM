from pydub import AudioSegment

# 加载两个音频文件（它们需要是 WAV 格式）
voice = AudioSegment.from_wav("tortoise_output.wav")
music = AudioSegment.from_wav("musicgen_output.wav")

# 如果音乐比语音短，可以循环铺满
if len(music) < len(voice):
    music = music * (len(voice) // len(music) + 1)

# 裁剪音乐长度与语音对齐
music = music[:len(voice)]

# 混合（-5 dB 为人声降低音量，避免盖住背景音乐）
mixed = music.overlay(voice - 5)

# 导出混合结果
mixed.export("final_mix.wav", format="wav")
print("✅ 混音完成，已保存为 final_mix.wav")
