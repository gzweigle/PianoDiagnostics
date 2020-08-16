# Gregary C. Zweigle
# 2020
import rtmidi
import time

# How long to wait after hitting a MIDI note before adjusting the volume.
MIDI_WAIT_SECONDS = 1

# TODO -
# MIDI is still not super reliable. Sometimes it doesn't play a note
# at all. For now, if still don't have a sound within 10 seconds,
# try again.
MIDI_MAX_WAIT_SECONDS = 10

# Maximum amount can increase the volume each time.
MAX_MIDI_CHANGE = 1.15

# Limit high value.
MAX_MIDI_VOLUME = 127

class Midi:

    def __init__(self, channel, peak_percent, must_exceed, cannot_exceed):
        self.played_note = 0
        self.channel = channel
        self.running_peak = 0
        self.peak_percent = peak_percent
        self.must_exceed = must_exceed
        self.cannot_exceed = cannot_exceed
        self.volume = 90
        self.note_is_being_played = False

    def startup_midi(self):
        self.driver = rtmidi.MidiOut()
        self.driver.open_port(self.channel)

    def send_note(self, play_midi, note_number):
        # Once issue the note, do not allow a new note
        # until after the note has been released.
        if play_midi and not self.note_is_being_played:
            # Add 20 as lowest A on piano is MIDI value 21.
            # And, most charts show lowest A on piano as note #1.
            self.played_note = note_number + 20
            # The MIDI control code 0x90 is for a note press.
            control_code = 0x90 + self.channel
            note_on = [control_code, self.played_note, self.volume]
            print("MIDI ON = {0}".format(note_on))
            self.driver.send_message(note_on)
            self.time_start = time.time()
            self.running_peak = 0
            self.note_is_being_played = True

    def release_note(self):
        if self.note_is_being_played:
            # The MIDI control code 0x80 is for a note release.
            control_code = 0x80 + self.channel
            note_off = [control_code, self.played_note, 127]
            print("MIDI OFF = {0}".format(note_off))
            self.driver.send_message(note_off)
            self.note_is_being_played = False

    def retry_if_note_did_not_trigger(self, play_midi, peak):
        if play_midi:
            if peak > self.running_peak:
                self.running_peak = peak
            # Wait to see if note was caught by the state machine trigger.
            if (time.time() - self.time_start) > MIDI_WAIT_SECONDS:
                # Now make sure the original note strike has decayed
                # sufficiently that it won't impact the recording of the restrike.
                if (peak < self.running_peak * self.peak_percent or
                (time.time() - self.time_start) > MIDI_MAX_WAIT_SECONDS):
                    # TODO - It would be nice if release_note was put after
                    # the time exceeded but before the decay check. Then,
                    # the note would decay even faster. But, once release the
                    # note, the next time through monitor state, it gets
                    # played again!  So, can't release it until after all
                    # of the if statements of this section are checked.
                    self.release_note()
                    # Avoid any possible divide by 0 issues.
                    if self.running_peak == 0:
                        self.running_peak = 1
                    if self.running_peak > self.cannot_exceed:
                        # Lower the volume a bit.
                        self.volume *= 0.95 * self.cannot_exceed / self.running_peak
                    elif self.running_peak < self.must_exceed:
                        # Raise the volume a bit.
                        volume_scale = 1.05 * self.must_exceed / self.running_peak
                        # If for some reason the MIDI fails to produce any sound
                        # (so, running_peak is very small), don't want the volume
                        # to hit full scale. So, limit how much can change.
                        if volume_scale > MAX_MIDI_CHANGE:
                            volume_scale = MAX_MIDI_CHANGE
                        self.volume *= volume_scale
                        if self.volume > MAX_MIDI_VOLUME:
                            self.volume = MAX_MIDI_VOLUME
                    else:
                        # If get here, things are probably really broken.
                        # So, just reset the volume.
                        self.volume = 90