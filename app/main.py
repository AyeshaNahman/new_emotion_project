from fastapi import FastAPI, UploadFile, File, HTTPException
import librosa
import numpy as np
import tensorflow as tf
from .feature_extraction import extract_features
import io

app = FastAPI()

# Load the model (ensure it's in the 'model/' folder)
try:
    model = tf.keras.models.load_model('model/my_model.h5')
except Exception as e:
    print(f"Warning: Could not load model: {e}")
    model = None

@app.post("/predict")
async def predict(audio: UploadFile = File(...)):
    # Check if the uploaded file is a .wav file
    if not audio.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are allowed.")

    # Read the audio file data
    audio_data = await audio.read()
    print(f"Received audio file of size: {len(audio_data)} bytes")

    try:
        # Extract features from the uploaded audio file
        features = extract_features(audio_data)
        print("Extracted features:", features)  # Debugging: log extracted features

        # Make a prediction using the model
        prediction = model.predict(np.expand_dims(features, axis=0))
        print("Prediction:", prediction)  # Debugging: log prediction

        return {"prediction": prediction.tolist()}

    except Exception as e:
        print("Error:", e)  # Log any error that occurs
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
