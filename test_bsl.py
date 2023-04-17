import bsl
from bsl import StreamPlayer

if __name__ == '__main__':
    dataset = bsl.datasets.eeg_resting_state.data_path()
    player = StreamPlayer('StreamPlayer', dataset)
    player.start()