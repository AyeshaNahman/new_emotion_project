import librosa
import numpy as np

def extract_features(audio_data):
    # Load the audio file from the binary data
    y, sr = librosa.load(audio_data, sr=None)

    # Extract MFCC (Mel-frequency cepstral coefficients) features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Return the mean of each MFCC feature
    return mfcc.mean(axis=1)
