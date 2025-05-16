import torch
import librosa
import numpy as np
from torch import autocast
from contextlib import nullcontext
import sys
import os
sys.path.insert(0, '/opt/EfficientAT-main/')
from video_updates import update_audio_tag
from models.MobileNetV3 import get_model as get_mobilenet, get_ensemble_model
from models.preprocess import AugmentMelSTFT
from helpers.utils import NAME_TO_WIDTH, labels

class EATagger:
   
    def __init__(self,
        model_name=None,
        ensemble=None,
        device='cuda',
        sample_rate=32000,
        window_size=800,
        hop_size=320, 
        n_mels=128):

        self.device = torch.device('cuda') if device == 'cuda' and torch.cuda.is_available() else torch.device('cpu')
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.hop_size = hop_size
        self.n_mels = n_mels

        # load pre-trained model
        if ensemble is not None:
            self.model = get_ensemble_model(ensemble)
        elif model_name is not None:
            self.model = get_mobilenet(width_mult=NAME_TO_WIDTH(model_name), pretrained_name=model_name)
        else:
            raise ValueError('Please provide a model name or an ensemble of models')

        self.model.to(self.device)
        self.model.eval()

        # model to preprocess waveform into mel spectrograms
        self.mel = AugmentMelSTFT(n_mels=self.n_mels, sr=self.sample_rate, win_length=self.window_size, hopsize=self.hop_size)
        self.mel.to(self.device)
        self.mel.eval()

    def tag_audio_window(self, audio_path, window_size=20.0, hop_length=10.0):
       

        # load audio file
        (waveform, _) = librosa.core.load(audio_path, sr=self.sample_rate, mono=True)
        waveform = torch.from_numpy(waveform[None, :]).to(self.device)

        # analyze the audio file in windows, pad the last window if needed
        window_size = int(window_size * self.sample_rate)
        hop_length = int(hop_length * self.sample_rate)
        n_windows = int(np.ceil((waveform.shape[1] - window_size) / hop_length)) + 1
        waveform = torch.nn.functional.pad(waveform, (0, n_windows * hop_length + window_size - waveform.shape[1]))


        with torch.no_grad(), autocast(device_type=self.device.type) if self.device.type == 'cuda' else nullcontext():
            tags = []
            for i in range(n_windows):
                start = i * hop_length
                end = start + window_size
                spec = self.mel(waveform[:, start:end])
                preds, features = self.model(spec.unsqueeze(0))
                preds = torch.sigmoid(preds.float()).squeeze().cpu().numpy()
                sorted_indexes = np.argsort(preds)[::-1]

                # Print audio tagging top probabilities
                tags.append({
                    'start': start / self.sample_rate,
                    'end': end / self.sample_rate,
                    'tags': [{
                        'tag': labels[sorted_indexes[k]],
                        'probability': preds[sorted_indexes[k]]
                    } for k in range(10)]
                })

                
                print(f'\rProgress: {i+1}/{n_windows}', end='')
            print()


        return tags
        



file_path="/home/dimineno/Downloads/ZoomFM.wav"
# load the model
model = EATagger(model_name='mn10_as', device='cuda' )

# tag the audio file
tags = model.tag_audio_window(file_path, window_size=10, hop_length=2.5)

# Define the confidence threshold
threshold = 0.8

# List to store filtered results
filtered_results = []

# Set to track unique tags across all windows
seen_tags = set()

# Process each window
for window in tags:
    # Filter tags that have a probability above the threshold
    filtered_tags = [
        tag for tag in window['tags'] if tag['probability'] >= threshold and tag['tag'] not in seen_tags
    ]
    
    # Add the tags to the seen_tags set to avoid duplicates
    for tag in filtered_tags:
        seen_tags.add(tag['tag'])

    # If there are any tags left in the window after filtering, add the window to the result
    if filtered_tags:
        filtered_results.append({
            'start': window['start'],
            'end': window['end'],
            'tags': filtered_tags
        })

# Print the filtered results
for window in filtered_results:
    print(f"Window: {window['start']} - {window['end']}")
    for tag in window['tags']:
        print(f"    {tag['tag']}: {tag['probability']}")
    print()