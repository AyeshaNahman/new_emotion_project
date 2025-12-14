const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const fileName = document.getElementById('fileName');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const error = document.getElementById('error');

// Use same origin as the served frontend (works locally and in production)
const API_URL = window.location.origin;

// Enable upload button when file is selected
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        fileName.textContent = `Selected: ${file.name}`;
        uploadBtn.disabled = false;
    }
});

// Upload and detect emotion
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    // Validate file type
    if (!file.name.endsWith('.wav')) {
        showError('Please select a .wav file');
        return;
    }

    // Show loading state
    loading.classList.remove('hidden');
    result.classList.add('hidden');
    error.classList.add('hidden');

    try {
        const formData = new FormData();
        formData.append('audio', file);

        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error detecting emotion');
        }

        const data = await response.json();
        console.log('API Response:', data);
        console.log('Prediction array:', data.prediction);
        displayResult(data.prediction);

    } catch (err) {
        showError(err.message);
        console.error('Error:', err);
    } finally {
        loading.classList.add('hidden');
    }
});

function displayResult(prediction) {
    // Emotion classes - customize these based on your model
    const emotions = [
        'Angry',
        'Disgust',
        'Fear',
        'Happy',
        'Neutral',
        'Sad',
        'Surprised',
        'Calm'
    ];

    // Get the emotion with highest confidence
    console.log('Raw prediction:', prediction);
    console.log('Prediction type:', typeof prediction);
    console.log('Is array?:', Array.isArray(prediction));
    
    const maxValue = Math.max(...prediction);
    const maxIdx = prediction.findIndex(val => val === maxValue);
    const emotion = emotions[maxIdx] || 'Unknown';
    const confidence = (maxValue * 100).toFixed(1);
    
    console.log('Max value:', maxValue);
    console.log('Max index:', maxIdx);
    console.log('Emotion:', emotion);
    console.log('Confidence:', confidence);

    document.getElementById('emotionName').textContent = emotion;
    document.getElementById('emotionConfidence').textContent = `Confidence: ${confidence}%`;

    result.classList.remove('hidden');
}

function showError(message) {
    error.textContent = '❌ ' + message;
    error.classList.remove('hidden');
}

function resetForm() {
    fileInput.value = '';
    fileName.textContent = '';
    uploadBtn.disabled = true;
    result.classList.add('hidden');
    error.classList.add('hidden');
}

console.log('Emotion Detector Frontend Loaded');
console.log('API URL:', API_URL);
