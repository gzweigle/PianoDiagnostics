# Gregary C. Zweigle
# 2020
import fifo
import numpy as np
import pyaudio
import time

class AudioInOut:

    def __init__(self, rate, chunk):
        self.fifo = fifo.Fifo(20)
        self.width = 2
        self.channels = 2
        self.rate = rate
        self.chunk = chunk
        self.audio_driver_is_running = False

    def start_driver_if_not_already_started(self):
        if not self.audio_driver_is_running:
            self.pa = pyaudio.PyAudio()
            self.stream = self.pa.open(
                format = self.pa.get_format_from_width(self.width),
                channels = self.channels,
                rate = self.rate,
                input = True,
                output = True,
                frames_per_buffer = self.chunk,
                stream_callback = self.callback)
            self.stream.start_stream()
        self.audio_driver_is_running = True

    # Received values are integers in range [-32768, 32767].
    # Channels are interleaved, first right then left.
    def get_data_from_audio_driver(self):
        self.start_driver_if_not_already_started()
        valid = False
        data_interleaved = 0
        while not valid:
            data_interleaved, valid = self.fifo.get()
            # Without this it seems to hit the try/except in get()
            # too fast and program execution gets erratic.
            waste_time = np.zeros((1000,))
        data_interleaved = data_interleaved.astype(float)
        data_r = data_interleaved[::2]
        data_l = data_interleaved[1::2]
        return (data_l, data_r)

    def callback(self, in_data, frame_count, time_info, status):

        jack_data = np.fromstring(in_data, dtype=np.int16)
        if jack_data.shape[0] != 2*self.chunk:
            # Fix annoying startup transient.
            jack_data = np.zeros((2*self.chunk,)).astype('int16')
        self.fifo.put(jack_data)

        # Send zeros to the speakers.
        audio_out = np.zeros((2*self.chunk,)).astype('int16')

        return audio_out, pyaudio.paContinue