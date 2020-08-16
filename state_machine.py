# Gregary C. Zweigle
# 2020

# TODO - This class is too complicated.

import audio_in_out
import peak_trigger
import file_in_out
import file_name
import midi

import numpy as np
import os

# Stop recording when get smaller than this ratio of the original peak.
PEAK_PERCENT = 0.01

# In any case, never record longer than this number of seconds.
MAX_RECORD_TIME = 10

# In any case, record at least this number of seconds.
MIN_RECORD_TIME = 0.5

# Initially I am using my Nord Stage 3 and it requires channel 1.
# TODO - This should be a user input.
MIDI_CHANNEL = 1

class StateMachine:

    def __init__(self, must_exceed, cannot_exceed, rate, chunk):
        self.pk = peak_trigger.PeakTrigger(must_exceed, cannot_exceed)
        self.fio = file_in_out.FileInOut(rate)
        self.fnm = file_name.FileName()
        self.midi = midi.Midi(MIDI_CHANNEL, PEAK_PERCENT, must_exceed, cannot_exceed)
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            # Server is initialized twice by Flask and that
            # makes the Midi driver unhappy. So, do not start
            # the drive on the second time through.
            self.midi.startup_midi()

        self.state = 'start'
        # Messages for server to display on the web browser.
        self.status_msg = 'Initialized'
        self.error_msg = 'No errors'
        self.peak_msg = '0'
        self.original_peak_value = 0
        # When starting to record, also save the chunk immediately before
        # threshold was crossed to catch initiating portion of waveform.
        self.last_data_l = np.zeros((chunk,))
        self.last_data_r = np.zeros((chunk,))

    def state_machine(self, record_mode, record_directory, record_start_note,
    record_midi, data_l, data_r):

        recording_now = False
        if self.state == 'start':
            self.state_start(record_start_note)
            if record_mode:
                self.state = 'monitor'
            else:
                self.state = 'start'

        elif self.state == 'monitor':

            # When MIDI automatically is generating the notes,
            # strike the note once here,
            # at the start of the monitoring.
            self.midi.send_note(record_midi, self.fnm.get_note_number())

            # If the MIDI note was not in the trigger range, try again.
            # TODO - Could be simplified if merge with send_note()?
            self.midi.retry_if_note_did_not_trigger(
                record_midi, max(np.absolute(data_l)))

            # When detect a note played and its in the proper
            # range, then start to record it to a file.
            (could_not_open_file, recording_now) = \
                self.state_monitor(record_directory, data_l, data_r)

            if could_not_open_file:
                self.state = 'start'
            elif recording_now:
                self.state = 'record'
            else:
                self.state = 'monitor'

        elif self.state == 'record':
            recording_now = self.state_record(data_l, data_r)
            if not recording_now:
                self.state = 'advance'
            else:
                self.state = 'record'

        elif self.state == 'advance':
            done = self.state_advance()
            if not record_mode:
                self.state = 'start'
            elif done:
                self.state = 'done'
            else:
                self.state = 'monitor'

        else:
            self.done_state()
            self.state = 'done'

        # When first start recording a new note, save the present
        # audio data plus the previous chunk of audio data.
        # This ensures any signal prior to the initiating peak is captured.
        self.last_data_l[:] = data_l
        self.last_data_r[:] = data_r

        return (recording_now, self.status_msg, self.error_msg, self.peak_msg)

    # Each is for the actions of one state.
    def state_start(self, record_start_note):
        self.status_msg = 'Nothing happening here'
        self.pk.set_peak(0)
        self.fnm.initialize_file_name(record_start_note)

    def done_state(self):
        self.status_msg = 'We are done!!'
        self.peak_msg = -1
        # Do not change self.error_msg, so any errors not lost.

    def state_monitor(self, directory, data_l, data_r):
        (file_name_l, file_name_r) = self.fnm.get_file_name()
        self.status_msg = ('Waiting for note, L of L/R to ' +
        directory + '/' + file_name_l)
        self.peak_msg = str(self.pk.peak(data_l, data_r))
        if self.pk.is_in_trigger_range(data_l, data_r):
            if self.fio.open_file(directory, file_name_l, file_name_r, False):
                recording_now = True
                could_not_open_file = False
                # Store previous chunk first to catch initiating waveform.
                self.fio.write(self.last_data_l, self.last_data_r)
                peak_value0 = self.fio.get_last_wrote_peak()
                # Now store the present chunk.
                self.fio.write(data_l, data_r)
                peak_value1 = self.fio.get_last_wrote_peak()
                self.original_peak_value = max([peak_value0, peak_value1])
                self.error_msg = 'No errors'
            else:
                recording_now = False
                could_not_open_file = True
                self.error_msg = ('Unable to open file (L)' + directory +
                '/' + file_name_l)
        else:
            recording_now = False
            could_not_open_file = False
        return(could_not_open_file, recording_now)

    def state_record(self, data_l, data_r):
        self.fio.write(data_l, data_r)
        record_duration = self.fio.get_record_seconds()
        self.status_msg = 'Recording note, time = ' + str(record_duration)
        self.peak_msg = str(self.pk.peak(data_l, data_r))

        peak_value = self.fio.get_last_wrote_peak()
        record_duration = self.fio.get_record_seconds()
        if record_duration > MIN_RECORD_TIME and \
            (peak_value <= PEAK_PERCENT*self.original_peak_value or
            record_duration > MAX_RECORD_TIME):
            recording_now = False
        else:
            recording_now = True
        return recording_now

    def state_advance(self):
        self.status_msg = 'Advancing to next note'
        self.midi.release_note()
        if not self.fio.close_file():
            self.error_msg = 'Unable to close file'
        self.fnm.advance_file_name()
        self.pk.set_peak(0)
        if self.fnm.check_if_finished_all_notes():
            return True
        else:
            return False