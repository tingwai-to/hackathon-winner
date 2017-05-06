from flask import Flask, render_template
from sklearn.externals import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict/<text>')
def predict(text):
    return str(model.predict_proba([text])[0][1])


if __name__ == '__main__':
    app.run()
