import time
import numpy as np
from bsl.utils import Timer
from keras import backend as K
from keras.models import model_from_json
from sklearn.preprocessing import StandardScaler
from buffer import Buffer
from bsl import StreamReceiver

def predict_eeg(stream_name):
    # Define the custom activation functions
    def square(x):
        return K.square(x)

    def log(x):
        return K.log(K.clip(x, min_value=1e-7, max_value=10000))

    # Load the model
    with open('/Users/mitchell/Desktop/Workspace/BCI/zy/model_shallowConvNet.json', 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json, custom_objects={'square': square, 'log': log})
    # load optimal weights
    model.load_weights('/Users/mitchell/Desktop/Workspace/BCI/zy/model_shallowConvNet.h5')

    sr = StreamReceiver(bufsize=1, winsize=1, stream_name=stream_name)
    time.sleep(1)  # wait to fill LSL inlet.
    sr.acquire()

    # Create buffer
    desired_channels = [
        'EEG-Fz',
        'EEG-0',
        'EEG-1',
        'EEG-2',
        'EEG-3',
        'EEG-4',
        'EEG-5',
        'EEG-C3',
        'EEG-6',
        'EEG-Cz',
        'EEG-7',
        'EEG-C4',
        'EEG-8',
        'EEG-9',
        'EEG-10',
        'EEG-11',
        'EEG-12',
        'EEG-13',
        'EEG-14',
        'EEG-Pz',
        'EEG-15',
        'EEG-16'
    ]
    buffer_duration = 251 / 250
    buffer = Buffer(buffer_duration, sr, desired_channels)

    # Start by filling once the entire buffer (to get rid of the initialization 0)
    timer = Timer()
    while timer.sec() <= buffer_duration:
        buffer.update()

    # Acquire during 10 seconds and plot every 1 seconds
    idx_last_plot = 1
    timer.reset()

    X_together = []  # Initialize an empty list to store multiple trials

    start_time = time.time()
    while timer.sec() <= 10: # TODO: Set time interval of data segment
        buffer.update()
        if timer.sec() // 1 == idx_last_plot:
            data = buffer.data
            scaler = StandardScaler()
            scaler.fit(data)
            data_scaled = scaler.transform(data)
            data = data_scaled / 540
            X = data.reshape(1, len(desired_channels), 251)
            X_together.append(X[0])
            idx_last_plot += 1

    # Convert the list of trials into a numpy array with the desired format (trials, channels, samples)
    X_together = np.array(X_together)

    # Make prediction on test set
    probs = model.predict(X_together)
    preds = probs.argmax(axis=-1)

    end_time = time.time()
    print(end_time - start_time)

    return X_together, probs

if __name__ == '__main__':
    stream_name = 'StreamTest'
    X_together, probs = predict_eeg(stream_name)
    print("X_together shape:", X_together.shape)
    print(X_together)
    print(len(X_together[0]))
    print(probs)
