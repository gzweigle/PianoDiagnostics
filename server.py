# Gregary C. Zweigle
# 2020

import audio_in_out
import state_machine
import numpy as np

# A new set of values is received every CHUNK/RATE seconds.
# For CHUNK=4096, RATE=44100 values, this is 92.88 milliseconds.
CHUNK = 4096
RATE = 44100

# As this value increases, the displayed data (not data written to files)
# becomes more coarse and also moves slower on the screen.
DOWNSAMPLE = 1024

# These will need to be adjusted based on the microphone setup.
MUST_EXCEED_VALUE = 1000
CANNOT_EXCEED_VALUE = 1500

class Server:

    def __init__(self):
        self.aio = audio_in_out.AudioInOut(RATE, CHUNK)
        self.sm = state_machine.StateMachine(MUST_EXCEED_VALUE,
        CANNOT_EXCEED_VALUE, RATE, CHUNK)

    def server(self, socket_io, record_mode, record_directory,
    record_start_note, record_midi):

        # Get complete data from audio driver.
        (data_l, data_r) = self.aio.get_data_from_audio_driver()

        # Create a modified downsampled verison.
        # Modified means: the downsampled value is the maximum from the range.
        # This modified downsampled version is for display purposes,
        # it is not saved to disk.
        data_l_down = []
        data_r_down = []
        for k in range(0, CHUNK - DOWNSAMPLE, DOWNSAMPLE):
            data_l_down.append(self.return_posneg_max(data_l[k:k+DOWNSAMPLE]))
            data_r_down.append(self.return_posneg_max(data_r[k:k+DOWNSAMPLE]))

        (recording_now, status_msg, error_msg, peak_msg) = \
            self.sm.state_machine(record_mode, record_directory, 
            record_start_note, record_midi, data_l, data_r)

        # Send data to the client.
        transmit_dictionary = {
        'status_msg': status_msg,
        'error_msg' : error_msg,
        'peak_msg' : peak_msg,
        'recording_now' : recording_now,
        'range' : [MUST_EXCEED_VALUE, CANNOT_EXCEED_VALUE],
        'data_l_down' : data_l_down,
        'data_r_down' : data_r_down}
        socket_io.emit('data_from_server', transmit_dictionary)

    # Return largest abs value of array, with original sign.
    @staticmethod
    def return_posneg_max(an_array):
        max_pos = np.amax(an_array)
        max_neg = np.amin(an_array)
        if (max_pos > abs(max_neg)):
            return max_pos
        else:
            return max_neg