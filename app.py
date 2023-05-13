# server.py
from flask import Flask, jsonify
# from new_model import predict_eeg_events
from newest_bsl import predict_eeg
from flask_cors import CORS
from test_raw import get_raw_signal

app = Flask(__name__)
CORS(app)

print('test print')


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
    response = {'raw': raw_list}
    print('Parse to JSON...')
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5777)
