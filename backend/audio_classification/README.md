# Audio Classification
This folder contains the audio classification training pipeline used in the Aristotle TV project.  
The goal was to distinguish between **music**, **speech**, and **other audio** in educational media.
For more information go to the thesis.pdf

---

## Model Overview

- **Model Type**: Convolutional Neural Network (CNN)
- **Classes**: `music`, `speech`, `other`
- **Libraries Used**:
  - PyTorch (model architecture & training)
  - PyWavelets (Discrete Wavelet Transform)
  - scikit-learn (cross-validation, metrics)

---

## Feature Extraction

Feature extraction was performed by generating **wavelet-based spectrograms**.  
The audio signals were processed using **Discrete Wavelet Transform (DWT)** via the `PyWavelets` library to capture both frequency and time-localized information.




## Dataset

This project used the **LVLib SMO v2 dataset**, designed for general audio classification.

- Dataset link:  
  [https://m3c.web.auth.gr/research/datasets/lvlib-smo-v2-for-general-audio-classification/](https://m3c.web.auth.gr/research/datasets/lvlib-smo-v2-for-general-audio-classification/)

---
## Notes

- Trained model files are not included due to size.
- This module was developed as the **research component** of the thesis.
- A pretrained version of the model is used in the production pipeline.

---
