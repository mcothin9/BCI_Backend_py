def get_raw_signal():
    import mne

    filename = '../BCICIV_2a/A01T.gdf'
    raw = mne.io.read_raw_gdf(filename, preload=True)

    n_channels = raw.info['nchan']
    duration = raw.times[-1]
    sfreq = raw.info['sfreq']

    # Extract the data from the .gdf file
    data, times = raw[:, :]

    # Calculate the y-axis values for each second
    time_period = 0.1  # in 0.1 seconds
    samples_per_period = int(sfreq * time_period)
    y_values_per_second = []

    for start_sample in range(0, len(times), samples_per_period):
        end_sample = start_sample + samples_per_period
        period_data = data[:, start_sample:end_sample]
        y_values = period_data.mean(axis=1)  # mean value for each channel during the time period
        y_values_per_second.append(y_values.tolist())  # Convert the ndarray to a list

    return y_values_per_second
