import os
import librosa
import numpy as np

def calculate_snr(reference_path, test_path):
    clean, sr = librosa.load(reference_path, sr=None)
    test, _ = librosa.load(test_path, sr=sr)
    
    min_len = min(len(clean), len(test))
    clean = clean[:min_len]
    test = test[:min_len]

    noise = clean - test
    signal_power = np.sum(clean ** 2)
    noise_power = np.sum(noise ** 2) + 1e-8
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

denoised_dir = r"E:\MTMusic\CLIP_project\analysis_output\tmpv7g75q6z"
raw_dir = r"E:\MTMusic\CLIP_project\analysis_output\tmp7dkepiv2"

denoised_file = [f for f in os.listdir(denoised_dir) if f.endswith(".wav")][0]
raw_file = [f for f in os.listdir(raw_dir) if f.endswith(".wav")][0]

denoised_path = os.path.join(denoised_dir, denoised_file)
raw_path = os.path.join(raw_dir, raw_file)

snr = calculate_snr(raw_path, denoised_path)
print(f"Comparing:\nRaw     : {raw_file}\nDenoised: {denoised_file}\nSNR = {snr:.2f} dB")
