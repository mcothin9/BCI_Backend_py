import time

from bsl import StreamPlayer, StreamReceiver, datasets
from bsl.utils import Timer

def main():
    start_time = time.time()
    stream_name = 'StreamTest'
    fif_file = "/Users/mitchell/Desktop/Workspace/BCI/BCICIV_2a/A01T.fif"

    player = StreamPlayer(stream_name, fif_file)
    player.start()
    end_time = time.time()
    print(end_time - start_time)

if __name__ == '__main__':
    main()

