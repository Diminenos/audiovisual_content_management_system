import numpy as np
import pywt
import matplotlib.pyplot as plt
import librosa
import librosa.display
import torch

def process_audio_wavelet(signal,sr, wavelet='db4', level=6, block_size=512):
    """
    generate wavelet-based spectrogram function
    """
    
    signal = signal / np.max(np.abs(signal))
    n_blocks = len(signal) // block_size
    WSE_matrix = []

 
    for i in range(n_blocks):
        start = i * block_size
        end = start + block_size
        block = signal[start:end]

        # Perform wavelet decomposition for the block
        block_coeffs = pywt.wavedec(block, wavelet=wavelet, level=level)

        # Compute Wavelet Spectrum Envelope (WSE) for each band
        WSE_band = []
        for band_coeff in block_coeffs:
            power = np.mean(np.square(band_coeff))  
            WSE_band.append(10 * np.log10(power + 1e-10))  # Prevent log overflow

        WSE_matrix.append(WSE_band)
    WSE_matrix = np.array(WSE_matrix).T



    #print(WSE_matrix.shape)
    return WSE_matrix



# List of wav file paths and their corresponding labels
wav_files = [
    "C:/Users/User/Desktop/LVLib-SMO-2/music.wav",
    "C:/Users/User/Desktop/LVLib-SMO-2/speech.wav",
    "C:/Users/User/Desktop/LVLib-SMO-2/other.wav"
]

class_labels = ['music', 'speech', 'others']
label_to_index = {label: idx for idx, label in enumerate(class_labels)}  # Map labels to integers

features = []
labels = []

# Iterate over the WAV files and corresponding labels
for i in range(len(wav_files)):
    file = wav_files[i]
    label = class_labels[i]
    
    # Load the audio data
    audio_signal, sample_rate = librosa.load(file, sr=None)
    segment_duration = 3 # seconds
    overlap = 0.5  # 50% overlap
    segment_length = int(segment_duration * sample_rate)
    
    step = int(segment_length * (1 - overlap))

    segments = []
    for j in range(0, len(audio_signal) - segment_length + 1, step):
        segment = audio_signal[j:j+segment_length]
        #Check if the segment contains zero values
        if not np.any(segment != 0):
            continue  # Skip this segment
        
        segments.append(segment)
    print(len(segments))
    
    # Extract features and assign labels
    for segment in segments:
        
        WSE_matrix = process_audio_wavelet(segment, sample_rate)
        features.append(WSE_matrix)
        labels.append(label_to_index[label])



features = np.array(features, dtype=np.float32)  
labels = np.array(labels, dtype=np.int64)       


features_tensor = torch.tensor(features)        
labels_tensor = torch.tensor(labels)             

# Save  tensors 
torch.save({"features": features_tensor, "labels": labels_tensor}, "C:/Users/User/Desktop/create algorithm/spectrogram_dataset.pt")

print(f"Saved {features_tensor.shape[0]} samples with shape {features_tensor.shape[1:]} and labels.")