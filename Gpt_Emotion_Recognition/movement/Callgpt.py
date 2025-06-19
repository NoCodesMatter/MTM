import os
import json
import base64
import sys
import random
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    api_key="sk-TtxIcdKCWgHl1vgvB0C0796b081345E1999a9f2873F39277",
    base_url="https://api.gpt.ge/v1/"
)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def get_random_images(image_folder, num_images=20, prompt_text=None):
    if not prompt_text:
        prompt_text = (
            "以下是从一段视频中提取的多个代表性画面，请判断这段视频的整体情绪基调。\n"
            "从joy,anger,sadness,fear和inner peace这五个中选一个类型作为基调再给描述例如：Sadness:slow and emotional R&B song with a groovy beat and smooth synths\n"
            "不要输出其他解释或建议。"
        )

    all_images = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(image_folder, filename)
            all_images.append(image_path)
    
    # 随机选择20张图片
    selected_images = random.sample(all_images, min(num_images, len(all_images)))
    
    # 转换为GPT需要的格式
    image_content = []
    for image_path in selected_images:
        b64_image = encode_image_to_base64(image_path)
        image_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64_image}"
            }
        })
    
    return [{"type": "text", "text": prompt_text}] + image_content

def analyze_video_emotion_with_gpt(image_folder, save_to_txt=True):
    content = get_random_images(image_folder)
    print(f"🚀 正在处理随机选择的20张图片...")

    messages = [{"role": "user", "content": content}]
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
        timeout=120
    )

    result = response.choices[0].message.content

    if response.choices[0].finish_reason == "length":
        print("⏭️ 正在续写未完成回复...")
        messages.append({"role": "user", "content": "请继续刚才的分析"})
        continuation = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=2048
        )
        result += "\n（续写）\n" + continuation.choices[0].message.content

    if save_to_txt:
        output_path = os.path.join(image_folder, f"gpt_emotion_analysis.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n✅ 分析结果已保存到：{output_path}")

    return result

# 🧠 入口：从命令行获取视频名子文件夹
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ 用法错误：请提供关键帧文件夹名，如：python Callgpt.py Fear")
        sys.exit(1)

    video_name = sys.argv[1]
    folder_path = os.path.join("keyframes_output", video_name)

    if not os.path.isdir(folder_path):
        print(f"❌ 文件夹不存在：{folder_path}")
        sys.exit(1)

    result = analyze_video_emotion_with_gpt(folder_path)
    print("\n🎬 分析结果：\n")
    print(result)
