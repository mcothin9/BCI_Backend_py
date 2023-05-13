def read_data(stream_name, fif_file, desired_channels):
    player = StreamPlayer(stream_name, fif_file)
    player.start()
    sr = StreamReceiver(bufsize=1, winsize=1, stream_name=stream_name)
    time.sleep(1)  # wait to fill LSL inlet.

    buffer_duration = 5  # seconds
    buffer = Buffer(buffer_duration, sr, desired_channels)

    try:
        while True:
            buffer.update()
            data = buffer.data
            timestamps = buffer.timestamps

            # Get the last second of data
            one_second_data = data[-sr.fs:]
            one_second_timestamps = timestamps[-sr.fs:]

            # Reshape the data for the model
            one_second_data = one_second_data.T[np.newaxis, :, :]

            # Predict the class probabilities
            probas = model.predict(one_second_data)

            # Get the class with the highest probability
            predicted_class = np.argmax(probas)

            print(f"Predicted class: {predicted_class}, probabilities: {probas}")

            time.sleep(1)  # Wait for a second before updating the prediction

    except KeyboardInterrupt:
        print("Stopped.")

    finally:
        player.stop()
        sr.stop()


if __name__ == "__main__":
    stream_name = "eeg_stream"
    fif_file = "./data/sample_raw_data.fif"
    desired_channels = ['Fz', 'Cz', 'Pz', 'Oz', 'P3', 'P4', 'T7', 'T8']

    read_data(stream_name, fif_file, desired_channels)
