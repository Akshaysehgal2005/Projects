import pickle
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/', methods=['POST'])
def predict_category():
    
    #Get input from POST and preprocess
    data = request.get_json()
    inp = [[i for i in data.values()]]
    
    #Load and predict using model
    model = pickle.load(open('model.pkl', 'rb'))
    output = model.predict(inp)
    
    #Return output
    outdict = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    return jsonify(category=outdict.get(output[0]))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=5000)