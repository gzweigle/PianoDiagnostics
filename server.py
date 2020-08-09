# Gregary C. Zweigle
# 2020
import audio_in_out
import digital_signal_processing
import file_in_out
import file_name

import numpy as np

CHUNK = 1024
RATE = 44100
DOWNSAMPLE = 512
MUST_EXCEED_VALUE = 500
RECORD_TIME_IN_SECONDS = 5

class Server:

    def __init__(self):
        self.state = 'start'
        self.aio = audio_in_out.AudioInOut(RATE, CHUNK)
        self.dsp = digital_signal_processing.DigitalSignalProcessing(MUST_EXCEED_VALUE)
        self.fio = file_in_out.FileInOut(RATE)
        self.fnm = file_name.FileName()
        self.status_msg = 'Initialized'
        self.error_msg = 'No errors'
        self.peak_msg = '0'
        self.record_time = RECORD_TIME_IN_SECONDS

    def server(self, socket_io, record_mode, record_directory, record_start_note,
    playback_mode, playback_directory, playback_start_note) :

        # Want to send to client when recording.  So, set this in state
        # machine when recording.
        recording_now = False

        (data_l, data_r) = self.aio.get_data_from_audio_driver()

        data_l_list = []
        data_r_list = []
        for k in range(0, CHUNK, DOWNSAMPLE):
            data_l_list.append(data_l[k])
            data_r_list.append(data_r[k])
        data_l_down = np.asarray(data_l_list).astype(float)
        data_r_down = np.asarray(data_r_list).astype(float)

        # Each state consists of the actions of the state,
        # followed by the control path for the next state.
        # TODO - Next this whole thing needs to be moved out of here.
        if self.state == 'start':
            self.state_start(record_start_note)
            if record_mode: # When client says to record, move on!
                self.state = 'monitor'
            else:
                self.state = 'start'

        elif self.state == 'monitor':
            (could_not_open_file, recording_now, record_duration) = \
                self.state_monitor(record_directory, data_l, data_r)

            if could_not_open_file:
                self.state = 'start'
            elif recording_now:
                self.state = 'record'
            else:
                self.state = 'monitor'

        elif self.state == 'record':
            (recording_now, record_duration) = self.state_record(data_l, data_r)
            if record_duration >= self.record_time:
                self.state = 'advance'
            else:
                self.state = 'record'

        elif self.state == 'advance':
            self.state_advance()
            self.state = 'monitor'

        # Send data to the client.
        transmit_dictionary = {'status_msg': self.status_msg,
        'error_msg' : self.error_msg, 'peak_msg' : self.peak_msg,
        'recording_now' : recording_now,
        'data_l_down' : data_l_down.tolist(),
        'data_r_down' : data_r_down.tolist()}
        socket_io.emit('data_from_server', transmit_dictionary)


    # Each is for the actions of one state.
    def state_start(self, record_start_note):
        self.status_msg = 'Nothing happening here'
        self.dsp.reset_peak()
        self.fnm.initialize_file_name(record_start_note)

    def state_monitor(self, record_directory, data_l, data_r):
        (file_name_l, file_name_r) = self.fnm.get_file_name()
        self.status_msg = ('Waiting for note, will record to (L) ' +
        record_directory + '/' + file_name_l)
        self.peak_msg = str(self.dsp.peak(data_l, data_r))
        if self.dsp.got_signal(data_l, data_r):
            if self.fio.open_file(record_directory, file_name_l, file_name_r, False):
                recording_now = True
                could_not_open_file = False
                record_duration = self.fio.save(data_l, data_r)
                self.error_msg = 'No errors'
            else:
                recording_now = False
                could_not_open_file = True
                record_duration = 0
                self.error_msg = ('Unable to open file (L)' + record_directory +
                '/' + file_name_l)
        else:
            recording_now = False
            could_not_open_file = False
            record_duration = 0
        return(could_not_open_file, recording_now, record_duration)

    def state_record(self, data_l, data_r):
        record_duration = self.fio.save(data_l, data_r)
        recording_now = True
        self.status_msg = 'Recording note, time = ' + str(record_duration)
        self.peak_msg = str(self.dsp.peak(data_l, data_r))
        if record_duration >= self.record_time:
            if not self.fio.close_file():
                self.error_msg = 'Unable to close file'
        return(recording_now, record_duration)

    def state_advance(self):
        self.status_msg = 'Advancing to next note'
        self.fnm.advance_file_name()
        self.dsp.reset_peak()