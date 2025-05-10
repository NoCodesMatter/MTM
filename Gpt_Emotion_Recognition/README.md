# Video-based-Emotion-Recognition-Using-GPT
Generate emotion key words by sending video clips to ChatGPT

# Description

In this project i use the work of [keyframe-extraction-for-video-summarization](https://github.com/ttharden/Keyframe-Extraction-for-video-summarization) to pick up keyframes.
First, The large model TransNetV2 was utilized to conduct shot segmentations, and the large model CLIP was employed to extract semantic features for each frame within each shot. Second, an adaptive clustering method is devised to automatically determine the optimal clusters, based on which we performed candidate keyframe selection and redundancy elimination shot by shot. Finally, a keyframe set was obtained by concatenating keyframes of all shots in chronological order.

After that, call gpt4-turbo to recognize the emotion of video by sending him video clips. Other models should also work.

# Environment setting

First, conda create environment
```bash
conda env create --name keyframe python==3.10
conda activate keyframe
```

Then pull the project and download requirements
```bash
git clone https://github.com/shumu7Mushroom/Video-based-Emotion-Recognition-Using-GPT.git
cd Video-based-Emotion-Recognition-Using-GPT
pip install -r requirements.txt
```

By the way, if you havn't download ffmpeg in your computer, you can [download](https://www.ffmpeg.org/) it and add the path to your system's environment variables

# Use it 

_Step 1:_ Run pipeline.py to get the keyframe sequence
```bash
cd movement
python pipeline.py your_vedio_name
```

_Step 2:_ Run save.py to save the keyframes
```bash
python save.py your_vedio_name
```

_Step 3:_ Run Callgpt.py to call gpt to get emotion

Prompt are chageable, you can send anything you like. You need your own api_key and put it into the codes.
```bash
python Callgpt.py
```

# Acknowlegement

I refer the codes of following project

[CLIP](https://github.com/openai/CLIP)

[TransnetV2](https://github.com/soCzech/TransNetV2)

[keyframe-extraction-for-video-summarization](https://github.com/ttharden/Keyframe-Extraction-for-video-summarization)

# Reference
Tomas Soucek and Jakub Lokoc, “Transnet V2: an effective deep network architecture for fast shot transition detection,” arXiv:2008.04838, pp. 1–4, 2020.

Yang, An and Pan, Junshu and Lin, Junyang and Men, Rui and Zhang, Yichang and Zhou, Jingren and Zhou, Chang, "Chinese CLIP: Contrastive Vision-Language Pretraining in Chinese" arXiv preprint arXiv:2211.01335,2022

Tan, Kailong and Zhou, Yuxiang and Xia, Qianchen and Liu, Rui and Chen, Yong, “Large Model based Sequential Keyframe Extraction for Video Summarization,” arXiv preprint arXiv:2401.04962, pp. 1–11, 2024.












