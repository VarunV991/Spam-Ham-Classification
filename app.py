from flask import Flask, request, render_template
import sklearn
import pandas as pd
import joblib
import re

app = Flask(__name__)
model = joblib.load('models/modelNBCount.pkl')
vectorizer = joblib.load('models/count_vectorizer.pkl')

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/predict', methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
        #Input
        message = request.form['message']

        # Data Cleaning
        message = re.sub('[^a-zA-Z0-9]',' ',message)
        data = vectorizer.transform([message])
        
        #Prediction
        output = model.predict(data)
        
        #Output
        if(output==0):
            return render_template('result.html',prediction_text="The input message is NOT a spam")
        else:
            return render_template('result.html',prediction_text="The input message is a spam")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)