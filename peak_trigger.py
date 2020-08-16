# Gregary C. Zweigle
# 2020
import numpy as np
import time

# TODO - There is also peak checking in the Midi class.
class PeakTrigger:

    def __init__(self, must_exceed, cannot_exceed):
        self.peak_value = 0
        self.must_exceed = must_exceed
        self.cannot_exceed = cannot_exceed
        self.exceeded_max = False
        self.time_last = time.time()

    def is_in_trigger_range(self, data_l, data_r):

        peak_l = max(np.absolute(data_l))

        # If the peak exceeds the max, it must go below the min before
        # being considered again. This covers the corner case of a
        # note decaying into the range, when the requirement is to
        # record the note attacking into the range.
        return_value = True
        if peak_l > self.cannot_exceed:
            self.exceeded_max = True
            return_value = False
        if peak_l < self.must_exceed:
            return_value = False
        if peak_l < self.must_exceed/2:
            self.exceeded_max = False

        if return_value and not self.exceeded_max:
            return True
        else:
            return False

    # This is for display purposes only.
    def peak(self, data_l, data_r):
        present_peak = max([max(np.absolute(data_l)), max(np.absolute(data_r))])
        if self.return_true_every_second():
            self.set_peak(present_peak)
        elif present_peak > self.peak_value:
            self.peak_value = present_peak
            self.last_time = time.time() # Looks weird to reset on a peak.
        return self.peak_value

    def return_true_every_second(self):
        time_now = time.time()
        time_diff = time_now - self.time_last
        if time_diff > 1:
            self.time_last = time_now
            return True
        else:
            return False
    
    def set_peak(self, value):
        self.peak_value = value