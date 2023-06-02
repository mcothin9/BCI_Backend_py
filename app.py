# server.py
from flask import Flask, jsonify
from newest_bsl import predict_eeg
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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
    # interval[0] = min(np.amin(raw), interval[0])
    # interval[1] = max(np.amax(raw), interval[1])
    # print(f"Updated interval: {interval}")

    response = {'raw': raw_list}
    print('Parse to JSON...')
    return jsonify(response)


# Return probs and raw data in one response
@app.route('/data', methods=['GET'])
def get_data():
    data = predict_eeg('StreamTest')
    raw_list = data[0].tolist()
    probs_list = data[1].tolist()
    response = {'raw': raw_list, 'probs': probs_list}
    return jsonify(response)


# Return probs and raw data in one response
@app.route('/channel', methods=['GET'])
def get_channel():
    data = predict_eeg('StreamTest')
    raw_list = data[0].tolist()
    probs_list = data[1].tolist()
    # Assuming raw_list is of shape [10, channel_number, 251]
    channel_number = len(raw_list[0])
    # Assuming probs_list is of shape [10, class_number]
    class_number = len(probs_list[0])
    response = {'channelCount': channel_number, 'classCount': class_number}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5777)
