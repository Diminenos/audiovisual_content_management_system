import torch
import librosa
import ffmpeg
import os
import logging
import logger_config
import torch.nn as nn
import sys
import numpy as np
import pywt
import torch.nn.functional as F
from video_updates import update_audio_tag

# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)


# AudioCNN Model
class AudioCNN(nn.Module):
    def __init__(self, num_classes):
        super(AudioCNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),

            nn.Conv2d(16, 32, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),

            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 10))
        )

        self.flattened_size = 64 * 1 * 10
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(self.flattened_size, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

#Generate wavelet-based spectrogram
def process_audio_wavelet(signal, sr, wavelet='db4', level=6, block_size=512):
    
    signal = signal / np.max(np.abs(signal))
    n_blocks = len(signal) // block_size
    WSE_matrix = []

    for i in range(n_blocks):
        start = i * block_size
        end = start + block_size
        block = signal[start:end]

        # Perform wavelet decomposition
        block_coeffs = pywt.wavedec(block, wavelet=wavelet, level=level)
        WSE_band = [10 * np.log10(np.mean(np.square(band_coeff)) + 1e-10) for band_coeff in block_coeffs]
        WSE_matrix.append(WSE_band)

    return np.array(WSE_matrix).T

#Load trained model from checkpoint.
def load_audio_tag_model():
    model = AudioCNN(num_classes=3)
    best_model_cp = torch.load('/home/dimineno/consumer_celery/wavelet_model.pth', map_location=torch.device('cpu'))
    model.load_state_dict(best_model_cp['model_state_dict'])
    model.eval()
    return model

#Extract features from an audio file.
def extract_features(file_path):

    features = []

    # Load audio
    audio_signal, sample_rate = librosa.load(file_path, sr=22500)
    if len(audio_signal.shape) == 2:  # Convert stereo to mono
        audio_signal = audio_signal.mean(axis=1)

    segment_duration = 3  # seconds
    overlap = 0.5
    segment_length = int(segment_duration * sample_rate)
    step = int(segment_length * (1 - overlap))

    for j in range(0, len(audio_signal) - segment_length + 1, step):
        segment = audio_signal[j:j+segment_length]
        if np.any(segment != 0):  # Skip silent segments
            features.append(process_audio_wavelet(segment, sample_rate))

    # Convert to tensor
    features_tensor = torch.tensor(np.array(features, dtype=np.float32)).unsqueeze(1)
    return features_tensor

#Predict audio class
def predict_class(features, model):
    
    with torch.no_grad():
        output = model(features)

    probabilities = F.softmax(output, dim=1)
    mean_probs = np.mean(probabilities.numpy(), axis=0)

    # Get the top class
    class_labels = ["Music", "Speech", "Others"]
    top_class_name = class_labels[np.argmax(mean_probs)]
    
    return top_class_name

#Process audio and update the tag
def audio_tagging(post_id, file_path, model):
 
    try:
        file_name, file_extension = os.path.splitext(file_path)
        
        if file_extension.lower() == '.mp4':
            output_dir = '/home/dimineno/consumer_celery/'
            output_path = os.path.join(output_dir, os.path.basename(file_name) + '_audio.wav')

            os.makedirs(output_dir, exist_ok=True)
            ffmpeg.input(file_path).output(output_path, acodec='pcm_s16le', ar=16000).run(quiet=True, overwrite_output=True)

            features = extract_features(output_path)
            os.remove(output_path)
        else:
            features = extract_features(file_path)

        top_class_name = predict_class(features, model)
        top_class_name
        print(top_class_name)
        
        print(f'Task completed with result: {top_class_name}')
        
        update_audio_tag(post_id, [top_class_name])

    except Exception as e:
        logger.exception("Error in audio_tag_algorithm: %s", e)


if __name__ == '__main__':
    post_id = sys.argv[1]
    file_path = sys.argv[2]
    
    audio_model = load_audio_tag_model()
    audio_tagging(post_id, file_path, audio_model)
