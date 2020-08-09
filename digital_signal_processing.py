# Gregary C. Zweigle
# 2020
import numpy as np

class DigitalSignalProcessing:

    def __init__(self, must_exceed_value):
        self.peak_value = 0
        self.must_exceed_value = must_exceed_value

    def got_signal(self, data_l, data_r):
        # The peak is the smallest of the maximum values of the left and right.
        present_peak = min([max(np.absolute(data_l)), max(np.absolute(data_r))])
        if present_peak > self.must_exceed_value:
            return True
        else:
            return False

    def peak(self, data_l, data_r):
        present_peak = min([max(np.absolute(data_l)), max(np.absolute(data_r))])
        if present_peak > self.peak_value:
            self.peak_value = present_peak
        return self.peak_value
    
    def reset_peak(self):
        self.peak_value = 0