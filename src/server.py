from flask import Flask, request, jsonify
from tensorflow import keras
import pickle
import requests
import os
import time

server = Flask(__name__)

# Download model
modelFileUrl = os.environ.get('URL_MODEL')
modelFile = requests.get(modelFileUrl, allow_redirects=True)
open('model.h5', 'wb').write(modelFile.content)

# Download tokenizer
tokenizerFileUrl = os.environ.get('URL_TOKENIZER')
tokenizerFile = requests.get(tokenizerFileUrl, allow_redirects=True)
open('tokenizer.pkl', 'wb').write(tokenizerFile.content)

# Load model
model = keras.models.load_model('model.h5')

# Load tokenizer
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Set some parameters
SEQUENCE_LENGTH = 300
SENTIMENT_THRESHOLDS = (0.4, 0.7)

def decode_sentiment(score):
    label = "NEUTRAL"
    if score <= SENTIMENT_THRESHOLDS[0]:
        label = "NEGATIVE"
    elif score >= SENTIMENT_THRESHOLDS[1]:
        label = "POSITIVE"
    return label

def predict(text):
    start_at = time.time()
    x_test = keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    score = model.predict([x_test])[0]
    label = decode_sentiment(score)
    return {"label": label, "score": float(score) * 100, "treatment_time": time.time()-start_at}

@server.route('/api/v1/analyses', methods = ['POST'])
def analyses():
    content = request.get_json(silent=True)

    # Need to add security check on message

    message = content['message']
    result = predict(message)

    return jsonify(result)

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=os.environ.get('PORT'))