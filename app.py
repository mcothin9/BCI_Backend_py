# server.py
from flask import Flask, jsonify
from test_result_server import predict_eeg_events
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/probs', methods=['GET'])
def get_probs():
    print('App start...')
    # logging.basicConfig('After read file')
    probs = predict_eeg_events()
    print('Get probs')
    # Convert the numpy array to a Python list and wrap it in a dictionary
    probs_list = probs.tolist()
    response = {'probs': probs_list}
    # print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
