import librosa
import numpy as np
import io

def extract_features(audio_data):
    # Load the audio file from the binary data using BytesIO
    audio_stream = io.BytesIO(audio_data)
    y, sr = librosa.load(audio_stream, sr=None)

    # Extract multiple types of features to create a (130, 40) array
    # Extract MFCC (13 coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Shape: (13, n_frames)
    
    # Extract additional features to reach 40 total
    # Spectral features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=2048, n_chroma=12)  # (12, n_frames)
    
    # Spectral centroid (1 feature per frame)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]  # (n_frames,)
    
    # Spectral rolloff (1 feature per frame)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]  # (n_frames,)
    
    # Zero crossing rate (1 feature per frame)
    zcr = librosa.feature.zero_crossing_rate(y)[0]  # (n_frames,)
    
    # Temporal features - RMS energy
    rms = librosa.feature.rms(y=y)[0]  # (n_frames,)
    
    # Get the number of frames from MFCC
    n_frames = mfcc.shape[1]
    
    # Create feature matrix: transpose and combine all features
    mfcc = mfcc.T  # (n_frames, 13)
    chroma = chroma.T  # (n_frames, 12)
    
    # Reshape single features to match frame count
    spectral_centroid = spectral_centroid.reshape(-1, 1)  # (n_frames, 1)
    spectral_rolloff = spectral_rolloff.reshape(-1, 1)  # (n_frames, 1)
    zcr = zcr.reshape(-1, 1)  # (n_frames, 1)
    rms = rms.reshape(-1, 1)  # (n_frames, 1)
    
    # Concatenate: 13 + 12 + 1 + 1 + 1 + 1 = 29 features
    # Need 40 total, so add 11 more from MFCC derivatives or pad
    features = np.concatenate([
        mfcc,                    # 13
        chroma,                  # 12
        spectral_centroid,       # 1
        spectral_rolloff,        # 1
        zcr,                     # 1
        rms                      # 1
    ], axis=1)  # (n_frames, 29)
    
    # Add MFCC delta (rate of change) - 13 more features
    mfcc_delta = librosa.feature.delta(mfcc.T)  # (13, n_frames)
    mfcc_delta = mfcc_delta.T  # (n_frames, 13)
    
    # Now we have 29 + 13 = 42 features, take first 40
    features = np.concatenate([features, mfcc_delta], axis=1)[:, :40]  # (n_frames, 40)
    
    # Pad or truncate to 130 frames
    if features.shape[0] < 130:
        # Pad with zeros
        padded = np.zeros((130, 40))
        padded[:features.shape[0], :] = features
        features = padded
    else:
        # Truncate to 130 frames
        features = features[:130, :]
    
    return features
