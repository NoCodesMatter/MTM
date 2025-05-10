import os
import json
import base64
import sys
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    api_key="sk-TtxIcdKCWgHl1vgvB0C0796b081345E1999a9f2873F39277",
    base_url="https://api.gpt.ge/v1/"
)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def get_all_image_batches(image_folder, max_images_per_batch=20, prompt_text=None):
    if not prompt_text:
        prompt_text = (
            "以下是从一段视频中提取的多个代表性画面，请判断这段视频的整体情绪基调。\n"
            "从joy,anger,sadness,fear和inner peace这五个中选一个类型作为基调再给描述例如：Sadness:slow and emotional R&B song with a groovy beat and smooth synths\n"
            "不要输出其他解释或建议。"
        )

    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(image_folder, filename)
            b64_image = encode_image_to_base64(image_path)
            images.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64_image}"
                }
            })

    # 分批
    batches = [images[i:i + max_images_per_batch] for i in range(0, len(images), max_images_per_batch)]
    return [[{"type": "text", "text": prompt_text}] + batch for batch in batches]

def analyze_video_emotion_with_gpt(image_folder, save_to_txt=True):
    all_batches = get_all_image_batches(image_folder)
    result = ""

    for idx, batch_content in enumerate(all_batches):
        print(f"\n🚀 正在处理第 {idx+1}/{len(all_batches)} 批...")

        messages = [{"role": "user", "content": batch_content}]
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            timeout=120
        )

        partial_result = response.choices[0].message.content
        result += f"\n📦 第 {idx+1} 批结果：\n{partial_result}\n"

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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(image_folder, f"emotion_analysis_{timestamp}.txt")
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
