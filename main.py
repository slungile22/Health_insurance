from flask import Flask,render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app=Flask(__name__)
model = pickle.load(open('model.pkl','rb'))
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


standard_to=StandardScaler()
@app.route('/predict', methods=['POST'])
def predict():
    region_southeast=0
    region_southwest=0
    if request.method == 'POST':
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        sex_male = request.form['sex_male']
        if(sex_male=='male'):
            sex_male=1
        else:
            sex_male=0
        smoker_yes = request.form['smoker_yes']
        if(smoker_yes=='yes'):
            smoker_yes=1
        else:
            smoker_yes=0
        region_northwest = request.form['region_northwest']
        if(region_northwest=='northwest'):
            region_northwest=1
            region_southeast=0
            region_southwest=0
        elif(region_southeast=='southeast'):
            region_northwest=0
            region_southeast=1
            region_southwest=0
        elif(region_southwest=='southwest'):
            region_northwest=0
            region_southeast=0
            region_southwest=1
        else:
            region_northwest=0
            region_southeast=0
            region_southwest=0

        prediction=model.predict([[age,bmi,children,sex_male,smoker_yes,region_northwest,region_southeast,region_southwest]])
        output=round(np.expm1(prediction[0]),2)
        if output>0:
            return render_template('index.html', prediction_text='Your health insurance is $ {}'.format(output))
        else:
            return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
