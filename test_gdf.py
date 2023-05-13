import mne

# filename = '~/Desktop/Workspace/BCI/BCICIV_2a/A01E.gdf'
filename = '../BCICIV_2a/A01T.gdf'
raw = mne.io.read_raw_gdf(filename, preload=True)

# Get the number of channels
n_channels = raw.info['nchan']
print("Number of channels:", n_channels)

# Get the length of the whole line (duration in seconds)
duration = raw.times[-1]
print("Duration (seconds):", duration)

# Get the sampling frequency (number of samples per second)
sfreq = raw.info['sfreq']

# Extract the data from the .gdf file
data, times = raw[:, :]

# Calculate the y-axis values for each second
time_period = 1  # in seconds
samples_per_period = int(sfreq * time_period)
y_values_per_second = []

# Check y-axis range
y_min = 0
y_max = 0

for start_sample in range(0, len(times), samples_per_period):
    end_sample = start_sample + samples_per_period
    period_data = data[:, start_sample:end_sample]
    y_values = period_data.mean(axis=1)  # mean value for each channel during the time period
    y_values_per_second.append(y_values)

# Print the y-axis values for each second
for i, y_values in enumerate(y_values_per_second):
    for _, value in enumerate(y_values):
        if y_max < value: y_max = value
        if y_min > value: y_min = value
    print(f"Y-axis values at second {i}: {y_values}")

print('Max value: ', y_max)
print('Min value: ', y_min)

