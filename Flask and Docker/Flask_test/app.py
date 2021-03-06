from flask import Flask, render_template, request
from scipy.misc import imsave, imread, imresize
import numpy as np
import re
import sys
import os

sys.path.append(os.path.abspath('./model'))
from load import *

#init flask app

app = Flask(__name__)

global model, graph
model, graph = init()


def convertImage(imgData):
	imgstr = re.search(r'base64,(.*'.imgData1).group(1)
	with open('output.png', 'wb') as output:
		output.write(imgstr.decode('base64'))


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
	imgData = request.get_data()
	convertImage(imgData)
	x = imread('out.png', mode='L')
	x = np.invert(x)
	x = imresize(x, 28, 28)
	x = x.reshape(1, 28, 28, 1)
	with graph.as_default():
		out = model.predict(x)
		response = np.array_string(np.argmax(out, axis=0))
		return response


if __name__ = '__main__':
	port = int(os.environment.get('PORT',5000))
	app.run(host='0.0.0.0', port=port)