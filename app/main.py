from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import librosa
import numpy as np
import tensorflow as tf
from .feature_extraction import extract_features
import io

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend assets under /static to avoid shadowing API routes
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the main page at root
@app.get("/")
def root():
    return FileResponse("frontend/index.html")

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
        # Fail fast if model isn't loaded yet (e.g., before you add my_model.h5)
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded. Add model/my_model.h5 and restart.")

        # Extract features from the uploaded audio file
        features = extract_features(audio_data)
        print("Extracted features:", features)

        # Make a prediction using the model
        prediction = model.predict(np.expand_dims(features, axis=0))
        print("Prediction:", prediction)

        return {"prediction": prediction.tolist()}

    except Exception as e:
        print("Error:", e)  # Log any error that occurs
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
