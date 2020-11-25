from flask import Flask, request, jsonify
from tensorflow import keras

server = Flask(__name__)

# Load model
tokenizer = keras.preprocessing.text.Tokenizer()
model = keras.models.load_model('model-v1.h5')
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
    x_test = keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    score = model.predict([x_test])[0]
    label = decode_sentiment(score)
    return {"label": label, "percentage": float(score)}

@server.route('/api/v1/analyses', methods = ['POST'])
def analyses():
    content = request.get_json(silent=True)

    # Need to add security check on message

    message = content['message']
    print("Line to analyse : " + message)
    result = predict(message)

    return jsonify(result)

if __name__ == "__main__":
    server.run(host='0.0.0.0', debug=True)