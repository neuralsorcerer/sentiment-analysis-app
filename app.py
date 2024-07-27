from flask import Flask, request, render_template
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import tensorflow as tf

app = Flask(__name__)

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

def preprocess(text):
    inputs = tokenizer(text, return_tensors="tf", truncation=True, padding=True, max_length=512)
    return inputs

def predict_sentiment(text):
    inputs = preprocess(text)
    outputs = model(inputs)
    logits = outputs.logits
    predicted_class = tf.math.argmax(logits, axis=-1).numpy()[0]
    
    if predicted_class == 1:
        return "Positive"
    else:
        return "Negative"

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = ""
    if request.method == "POST":
        text = request.form["text"]
        sentiment = predict_sentiment(text)
    return render_template("index.html", sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)
