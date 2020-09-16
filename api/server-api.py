import numpy as np 
import os
from flask import Flask, request, render_template, make_response
import joblib
import pandas as pd

app = Flask(__name__, static_url_path = '/static')
model = joblib.load('model/final_model.pkl')
full_pipeline = joblib.load('model/pipeline.pkl')

@app.route('/')
def home():
    return render_template('template.html')


@app.route('/verify', methods = ['POST'])
def verify():
	age = float(request.form['AgeValue'])
	sex = request.form['gridRadioSex']
	height = float(request.form['HeightValue'])
	weight = float(request.form['WeightValue'])
	children = float(request.form['ChildrenValue'])
	smoker = request.form['gridRadioSmoker']
	region = request.form['gridRadioRegion']

	print('Dados de teste:')
	print('Age: {}'.format(age))
	print('Sex: {}'.format(sex))
	print('Height: {}'.format(height))
	print('Weight: {}'.format(weight))
	print('Children: {}'.format(children))
	print('Smoker: {}'.format(smoker))
	print('Region: {}'.format(region))
	
	BMI = weight/(height*10**-2)**2
	
	test = pd.DataFrame({
    'index' : [0],
    'age' : age,
    'sex' : sex,
    'bmi' : BMI,
    'bmi_cat' : bmi_categories(BMI),
    'children' : children,
    'smoker' : smoker,
    'region' : region
	})

	test.set_index('index')
	test.drop('index', axis = 1, inplace = True)
	
	test_prepared = full_pipeline.transform(test)


	charge_predicted = model.predict(test_prepared)[0]
	output_text = 'Predicted cost for the insurance: {0:.2f} dollars.'.format(charge_predicted)
	print(output_text)

	return render_template('template.html', output=output_text)

def bmi_categories(BMI):
	if BMI <= 18.5:
		return 'Underweight'
	elif 18.5 < BMI <= 24.9:
		return 'Normal'
	elif 24.9 < BMI <=29.9:
		return 'Overweight'
	else:
		return 'Obese'


if __name__ == '__main__':
	#port = int(os.environ.get('PORT', 5500))
	app.run('0.0.0.0', port = 80)