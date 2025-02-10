
import numpy as np
import pywt
import librosa
import librosa.display
import torch
import torch.nn as nn
import torch.nn.functional as F

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




audio_path = "C:/Users/User/Desktop/create algorithm/LVLib-SMO-2/speech1.wav"
features = []


# Load the audio data
audio_signal, sample_rate = librosa.load(audio_path, sr=22500)
if len(audio_signal.shape) == 2:  # Stereo audio
    audio_signal = audio_signal.mean(axis=1)
segment_duration = 3 # seconds
overlap = 0.5 # 50% overlap
segment_length = int(segment_duration * sample_rate)

step = int(segment_length * (1 - overlap))

segments = []
for j in range(0, len(audio_signal) - segment_length + 1, step):
    segment = audio_signal[j:j+segment_length]
    #Check if the segment contains zero values
    if not np.any(segment != 0):
        continue  # Skip this segment
    
    segments.append(segment)

# Extract features and assign labels
for segment in segments:
    
    WSE_matrix = process_audio_wavelet(segment, sample_rate)
    features.append(WSE_matrix)
    

features = np.array(features, dtype=np.float32)  
features_tensor = torch.tensor(features)         


#AudioCNN Model
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

features_tensor = features_tensor.unsqueeze(1)  # Adds a new dimension at index 1 (channels)

print(features_tensor.shape)

# Initialize Model

num_classes = 3
model = AudioCNN(num_classes)

    


# load the best model checkpoint
best_model_cp = torch.load('C:/Users/User/Desktop/wavelets/best_model.pth', map_location=torch.device('cpu'))
best_model_epoch = best_model_cp['epoch']
print(f"Best model was saved at {best_model_epoch} epochs\n")

#  Load the model parameters into the model
model.load_state_dict(best_model_cp['model_state_dict'])
model.eval()

#predict
with torch.no_grad():
    output = model(features_tensor)
    print(output)

probabilities = F.softmax(output, dim=1)

# Determine the predicted class for each sample (the class with the highest probability)
predicted_classes = torch.argmax(probabilities, dim=1)

# Convert the probabilities and predicted classes to numpy for further analysis
probabilities_np = probabilities.numpy()
predicted_classes_np = predicted_classes.numpy()

# Calculate the mean probabilities for each class
mean_probs = np.mean(probabilities_np, axis=0)

# Print out results
print(f"Class Probabilities:\n{probabilities_np}")
print(f"Predicted Classes: {predicted_classes_np}")
print(f"Mean Probabilities for each class: {mean_probs}")
