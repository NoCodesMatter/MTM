import os
import json
import base64
# import openai
from datetime import datetime

# 设置你的 OpenAI API Key
# openai.api_key = "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"
from openai import OpenAI
# client = OpenAI(api_key="sk-TtxIcdKCWgHl1vgvB0C0796b081345E1999a9f2873F39277")
client = OpenAI(
    api_key="sk-TtxIcdKCWgHl1vgvB0C0796b081345E1999a9f2873F39277",
    base_url="https://api.gpt.ge/v1/"
)


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def get_image_message_list(image_folder, prompt_text=None):
    message = []

    if not prompt_text:
        prompt_text = (
            "以下是从一段视频中提取的多个代表性画面，请判断这段视频的整体情绪基调。\n"
            "从joy,anger,sadness,fear和inner peace这五个中选一个类型作为基调再给描述例如：Sadness:slow and emotional R&B song with a groovy beat and smooth synths\n"
            "不要输出其他解释或建议。"
        )


    message.append({"type": "text", "text": prompt_text})

    for filename in sorted(os.listdir(image_folder)):
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(image_folder, filename)
            b64_image = encode_image_to_base64(image_path)
            message.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64_image}"
                }
            })

    return message

def analyze_video_emotion_with_gpt(image_folder, save_to_txt=True):
    messages = [
        {"role": "user", "content": get_image_message_list(image_folder)}
    ]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
        timeout=120
    )

    print(json.dumps(response.model_dump(), indent=2))
    result = response.choices[0].message.content

    if response.choices[0].finish_reason == "length":
        print("⏭️ 正在续写未完成回复...")
        # 把前面的 messages 原样继续发
        messages.append({"role": "user", "content": "请继续刚才的分析"})
        continuation = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=2048
        )
        result += "\n\n（续写）\n" + continuation.choices[0].message.content


    # 保存到 .txt 文件
    if save_to_txt:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(image_folder, f"emotion_analysis_{timestamp}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n✅ 分析结果已保存到：{output_path}")

    return result

# 示例用法（指向 frames_mixed 文件夹）
if __name__ == "__main__":
    # folder_path = "frames_mixed"  
    folder_path = "movement\keyframes_output" 
    # folder_path = "gpt_input_test" 
    result = analyze_video_emotion_with_gpt(folder_path)
    print("\n🎬 分析结果：\n")
    print(result)
