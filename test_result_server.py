
def predict_eeg_events():
    print('Before import')
    # logging.basicConfig('Before import')

    import os
    import mne
    import numpy as np
    from tensorflow.keras.models import model_from_json
    from tensorflow.keras import backend as K

    print('After import')
    # logging.basicConfig('After import')

    json_file_path = os.path.expanduser('~/Desktop/Workspace/BCI/model_EEGNet.json')
    weights_file_path = os.path.expanduser('~/Desktop/Workspace/BCI/model_EEGNet.h5')
    data_file_path = os.path.expanduser('~/Desktop/Workspace/BCI/sample_audvis_filt-0-40_raw.fif')

    with open(json_file_path, 'r') as json_file:
        loaded_model_json = json_file.read()

    print('After read file')
    # logging.basicConfig('After read file')

    model = model_from_json(loaded_model_json)
    model.load_weights(weights_file_path)

    K.set_image_data_format('channels_last')

    raw = mne.io.read_raw_fif(data_file_path, preload=True)
    raw.filter(2, None, method='iir')
    events = mne.find_events(raw)
    raw.info['bads'] = ['MEG 2443']  # set bad channels
    picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                           exclude='bads')
    epochs = mne.Epochs(raw, events, event_id={'audio left': 1, 'audio right': 2, 'visual left': 3, 'visual right': 4},
                        tmin=-0., tmax=1.0, proj=False, picks=picks, baseline=None, detrend=None, preload=True)
    preprocessed_data = epochs.get_data() * 1000

    print('After modelling')
    # logging.basicConfig('After modelling')

    # make prediction with model
    probs = model.predict(preprocessed_data)
    preds = probs.argmax(axis=-1)

    print('After predict')
    # logging.basicConfig('After predict')

    return probs
