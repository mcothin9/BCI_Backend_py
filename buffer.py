import numpy as np
from scipy.signal import butter, sosfilt, sosfilt_zi
from math import ceil

def create_bandpass_filter(low, high, fs, n):
    """
        Create a bandpass filter using a butter filter of order n.

        Parameters
        ----------
        low : float
            The lower pass-band edge.
        high : float
            The upper pass-band edge.
        fs : float
            Sampling rate of the data.
        n : int
            Order of the filter.

        Returns
        -------
        sos : array
            Second-order sections representation of the IIR filter.
        zi_coeff : array
            Initial condition for sosfilt for step response steady-state.
        """
    # Divide by the Nyquist frequency
    bp_low = low / (0.5 * fs)
    bp_high = high / (0.5 * fs)
    # Compute SOS output (second order sections)
    sos = butter(n, [bp_low, bp_high], btype="band", output="sos")
    # Construct initial conditions for sosfilt for step response steady-state.
    zi_coeff = sosfilt_zi(sos).reshape((sos.shape[0], 2, 1))

    return sos, zi_coeff


class Buffer:
    """
    A buffer containing filter data and its associated timestamps.

    Parameters
    ----------
    buffer_duration : float
        Length of the buffer in seconds.
    sr : bsl.StreamReceiver
        StreamReceiver connected to the desired data stream.
    desired_channels: list
        List of desired channels to be stored in the buffer.
    """

    def __init__(self, buffer_duration, sr, desired_channels):
        # Store the StreamReceiver in a class attribute
        self.sr = sr
        self.stream_name = "StreamTest"

        # Retrieve sampling rate and number of channels
        self.fs = int(self.sr.streams[self.stream_name].sample_rate)
        self.nb_channels = len(self.sr.streams[self.stream_name].ch_list) - 1

        # Define desired channels and get their indices

        self.desired_channels = desired_channels
        self.desired_indices = [i for i, name in enumerate(self.sr.streams[self.stream_name].ch_list) if
                                name in desired_channels]

        # Define duration
        self.buffer_duration = buffer_duration
        self.buffer_duration_samples = ceil(self.buffer_duration * self.fs)

        # Create data array
        self.timestamps = np.zeros(self.buffer_duration_samples)
        self.data = np.zeros((self.buffer_duration_samples, len(desired_channels)))
        # For demo purposes, let's store also the raw data
        self.raw_data = np.zeros((self.buffer_duration_samples, len(desired_channels)))

        # Create filter BP (1, 15) Hz and filter variables
        self.sos, self.zi_coeff = create_bandpass_filter(0.5, 100.0, self.fs, n=16)
        self.zi = None

    def update(self):
        """
        Update the buffer with new samples from the StreamReceiver. This method
        should be called regularly, with a period at least smaller than the
        StreamReceiver buffer length.
        """
        # Acquire new data points
        self.sr.acquire()
        data_acquired, ts_list = self.sr.get_buffer()
        self.sr.reset_buffer()

        if len(ts_list) == 0:
            return  # break early, no new samples

        # Remove trigger channel and select desired channels
        data_acquired = data_acquired[:, self.desired_indices]

        # Filter acquired data
        if self.zi is None:
            # Initialize the initial conditions for the cascaded filter delays.
            self.zi = self.zi_coeff * np.mean(data_acquired, axis=0)
        data_filtered, self.zi = sosfilt(self.sos, data_acquired, axis=0, zi=self.zi)

        # Roll buffer, remove samples exiting and add new samples
        self.timestamps = np.roll(self.timestamps, -len(ts_list))
        self.timestamps[-len(ts_list):] = ts_list
        self.data = np.roll(self.data, -len(ts_list), axis=0)
        self.data[-len(ts_list):, :] = data_filtered
        self.raw_data = np.roll(self.raw_data, -len(ts_list), axis=0)
        self.raw_data[-len(ts_list):, :] = data_acquired

