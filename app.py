# server.py
from flask import Flask, jsonify
# from new_model import predict_eeg_events
from newest_bsl import predict_eeg
from flask_cors import CORS
from test_raw import get_raw_signal
import numpy as np

app = Flask(__name__)
CORS(app)

print('test print')

interval = [np.inf, -np.inf]

@app.route('/probs', methods=['GET'])
def get_probs():
    print('App start...')
    # logging.basicConfig('After read file')
    probs = predict_eeg('StreamTest')[1]
    print('Get probs')
    # Convert the numpy array to a Python list and wrap it in a dictionary
    probs_list = probs.tolist()
    response = {'probs': probs_list}
    # print(response)
    return jsonify(response)


@app.route('/raw', methods=['GET'])
def get_raw():
    print('Start getting raw data...')
    raw = predict_eeg('StreamTest')[0]
    print("Return raw data...")
    raw_list = raw.tolist()

    # Update interval with min and max values from raw if they're smaller/larger respectively
    interval[0] = min(np.amin(raw), interval[0])
    interval[1] = max(np.amax(raw), interval[1])
    print(f"Updated interval: {interval}")

    response = {'raw': raw_list}
    print('Parse to JSON...')
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5777)
