import glob
import os
from keras import backend as K
import numpy as np


# Define the custom activation functions
def square(x):
    return K.square(x)


def log(x):
    return K.log(K.clip(x, min_value=1e-7, max_value=10000))


def predict_eeg_events():
    # Load the model
    from keras.models import model_from_json

    with open('/Users/mitchell/Desktop/Workspace/BCI/zy/model_shallowConvNet.json', 'r') as json_file:
        model_json = json_file.read()

    model = model_from_json(model_json, custom_objects={'square': square, 'log': log})
    model.load_weights('/Users/mitchell/Desktop/Workspace/BCI/zy/model_shallowConvNet.h5')


    all_file_path = glob.glob('/Users/mitchell/Desktop/Workspace/BCI/BCICIV_2a/*.gdf')
    # train_file_path = [i for i in all_file_path if 'T' in i.split('\\')[1]]
    train_file_path = [i for i in all_file_path if 'T' in os.path.split(i)[1]]
    # Read data and preprocess it
    X = read_data(train_file_path[0])

    # make prediction with model
    probs = model.predict(X)

    return probs


def read_data(file_path):
    import mne
    from mne import io

    data = mne.io.read_raw_gdf(file_path, preload=True)
    data.set_eeg_reference()
    data.filter(0.5, 100, method='iir')

    eog_channels = ['EOG-left', 'EOG-central', 'EOG-right']
    for ch_name in eog_channels:
        if ch_name in data.ch_names:
            data.set_channel_types({ch_name: 'eog'})

    picks = mne.pick_types(data.info, meg=False, eeg=True, eog=False, stim=False,
                           exclude=[])
    events, event_id = mne.events_from_annotations(data)
    selected_event_labels = ['769', '770', '771', '772']
    selected_event_id = {label: event_id[label] for label in selected_event_labels}

    selected_events = events[np.isin(events[:, 2], list(selected_event_id.values()))]
    epochs = mne.Epochs(data, selected_events, selected_event_id, tmin=-0., tmax=1, proj=False,
                        picks=picks, baseline=None, preload=True, verbose=False)
    labels = epochs.events[:, -1]
    X = epochs.get_data() * 1000

    return X
