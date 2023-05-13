import mne

# filename = '~/Desktop/Workspace/BCI/sample_audvis_filt-0-40_raw.fif'
filename = '~/Desktop/Workspace/BCI/BCICIV_2a/A01T.fif'
raw = mne.io.read_raw_fif(filename)

# Get the number of channels
n_channels = raw.info['nchan']
print("Number of channels:", n_channels)

# Get the length of the whole line (duration in seconds)
duration = raw.times[-1]
print("Duration (seconds):", duration)

# Get the sampling frequency (number of samples per second)
sfreq = raw.info['sfreq']

# Extract the data from the .fif file
data, times = raw[:, :]

# Calculate the y-axis values for each second
time_period = 1  # in seconds
samples_per_period = int(sfreq * time_period)
y_values_per_second = []

for start_sample in range(0, len(times), samples_per_period):
    end_sample = start_sample + samples_per_period
    period_data = data[:, start_sample:end_sample]
    y_values = period_data.mean(axis=1)  # mean value for each channel during the time period
    y_values_per_second.append(y_values)

# Print the y-axis values for each second
for i, y_values in enumerate(y_values_per_second):
    print(f"Y-axis values at second {i}: {y_values}")
