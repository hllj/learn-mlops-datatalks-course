from flask import Flask, request

from src.utils import load_pickle

app = Flask(__name__)
date = '2022-07-17'
dv = load_pickle(f'output/dv-{date}.pkl')
model = load_pickle(f'output/model-{date}.pkl')

def prepare_features(ride):
    features = {}
    features['PU_DO'] = f"{ride['PULocationID']}_{ride['DOLocationID']}"
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])
    

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_features(ride)
    pred = predict(features)
    return {
        'duration': pred,
        'model_version': date
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3500, debug=True)