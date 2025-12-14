# 🎵 Emotion Detector

A web-based audio emotion classification system using Machine Learning. Upload a .wav audio file and get real-time emotion detection across 8 emotion classes.

## Features

- 🎯 Real-time emotion classification from audio files
- 🎨 Beautiful, responsive web interface
- ⚡ Fast API backend using FastAPI
- 🤖 Deep learning model (TensorFlow/Keras)
- 📊 Audio feature extraction using librosa
- 🚀 Easy deployment

## Emotion Classes

The model classifies audio into 8 emotions:
1. Neutral
2. Calm
3. Happy
4. Sad
5. Angry
6. Fearful
7. Disgusted
8. Surprised

## Project Structure

```
emotion-detector/
├── backend/
│   ├── app/
│   │   ├── main.py          (FastAPI application)
│   │   ├── feature_extraction.py  (Audio feature extraction)
│   │   └── __init__.py
│   ├── model/               (Place trained model here)
│   │   └── my_model.h5      (Your trained model)
│   ├── requirements.txt
│   └── venv/                (Virtual environment)
├── frontend/
│   ├── index.html           (Web interface)
│   ├── styles.css           (Styling)
│   └── app.js               (Frontend logic)
└── README.md
```

## Installation

### Backend Setup

1. **Create virtual environment**
```bash
cd d:\new_emotion_project
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the API server**
```bash
python -m uvicorn app.main:app --reload
```

Server runs on: `http://localhost:8000`

### Frontend Setup

Open `frontend/index.html` in your browser or use a local server:

```bash
# Using Python
cd frontend
python -m http.server 8080

# Or use any local server (VS Code Live Server, etc.)
```

Frontend runs on: `http://localhost:8080`

## API Documentation

### Endpoints

#### POST `/predict`
Upload an audio file and get emotion classification.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Parameter: `audio` (file, .wav format)

**Response:**
```json
{
    "prediction": [0.1, 0.05, 0.02, 0.7, 0.05, 0.05, 0.02, 0.01]
}
```

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "audio=@path/to/audio.wav"
```

**Interactive API Docs:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Training Your Model

1. Prepare your training data in `.wav` format
2. Train your emotion classification model using TensorFlow
3. Save as `backend/model/my_model.h5`
4. The API will automatically load it on startup

## Usage

1. Start the backend server (see Installation)
2. Open the frontend in your browser
3. Click "Choose .wav file" to select an audio file
4. Click "Detect Emotion" to classify
5. View the emotion result with confidence percentage

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- TensorFlow/Keras - Deep learning
- Librosa - Audio processing
- NumPy - Numerical computing

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript (no dependencies)

## Environment Variables

No environment variables needed for local development.

For production, update `CORS` settings in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domain
)
```

## Deployment

### Deploy on Railway/Render

1. Push to GitHub (already done ✓)
2. Connect your repo to Railway or Render
3. Set start command: `uvicorn app.main:app --host 0.0.0.0`
4. Add environment variable: `PORT=8000`
5. Deploy!

### With Docker (optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t emotion-detector .
docker run -p 8000:8000 emotion-detector
```

## Contributing

Feel free to fork, modify, and improve!

## License

MIT License - feel free to use for personal and commercial projects
