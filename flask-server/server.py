import numpy as np
from flask import Flask, request, jsonify
import pickle
from test import test

app = Flask(__name__)

@app.route("/members",methods=['POST'])

def members():
   
    data = request.get_json(force=True)   
    prediction = test(data['area'],data['bhk'],data['bath'],data['loc'])
    print(prediction)
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(port=5000,debug = True)


    

