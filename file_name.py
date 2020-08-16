# Gregary C. Zweigle
# 2020

MAX_PIANO_NOTE = 88

# TODO - Should this move elsewhere?
class FileName:

    def __init__(self):
        self.note_number = 0
        self.file_name_l = 'EMPTY_L'
        self.file_name_r = 'EMPTY_R'

    def initialize_file_name(self, record_start_note):
        self.note_number = int(float(record_start_note))
        self.file_name_l = 'noteL' + str(self.note_number) + '.dat'
        self.file_name_r = 'noteR' + str(self.note_number) + '.dat'

    def advance_file_name(self):
        self.note_number = self.note_number + 1
        self.file_name_l = 'noteL' + str(self.note_number) + '.dat'
        self.file_name_r = 'noteR' + str(self.note_number) + '.dat'

    def get_file_name(self):
        return (self.file_name_l, self.file_name_r)

    def check_if_finished_all_notes(self):
        if self.note_number > MAX_PIANO_NOTE:
            return True
        else:
            return False

    # TODO - Originally it seemed like a good idea to track
    # notes in this class, but its too unrelated, need to move out.
    def get_note_number(self):
        return self.note_number