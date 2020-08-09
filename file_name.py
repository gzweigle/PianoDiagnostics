# Gregary C. Zweigle
# 2020

# All this does is create and increment file names.
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