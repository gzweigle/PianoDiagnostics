# Gregary C. Zweigle
# 2020
import numpy as np
import os

class FileInOut:

    def __init__(self, sample_rate):
        self.recording_seconds = 0
        self.successfully_opened_write_file = False
        self.sample_rate = sample_rate

    def open_file(self, directory, fname_l, fname_r, read_mode):
        self.recording_seconds = 0
        if not os.path.exists(directory):
            os.makedirs(directory)
        path_plus_name_l = directory + '\\' + fname_l
        path_plus_name_r = directory + '\\' + fname_r
        try:
            self.write_fp_l = open(path_plus_name_l, "w")
            try:
                self.write_fp_r = open(path_plus_name_r, "w")
                self.successfully_opened_write_file = True
            except:
                self.successfully_opened_write_file = False
        except:
            self.successfully_opened_write_file = False
        return self.successfully_opened_write_file
    
    def close_file(self):
        self.recording_seconds = 0
        if self.successfully_opened_write_file:
            try:
                self.write_fp_l.close()
                try:
                    self.write_fp_r.close()
                    return True
                except:
                    return False
            except:
                return False

    # Saving as text files for now.
    def save(self, data_l, data_r):
        if self.successfully_opened_write_file:
            self.recording_seconds = \
                self.recording_seconds + data_l.shape[0] / self.sample_rate
            np.savetxt(self.write_fp_l, data_l)
            np.savetxt(self.write_fp_r, data_r)
        return self.recording_seconds