import game_logic
from tkinter import filedialog
import sys
import fileinput


class GameLogParser:

    def __init__(self, log_name):
        self.log_name = log_name
        self.count_write = 1
        self.dimension = 0

    def save_file(self):
        file_name = filedialog.asksaveasfile(mode='w', defaultextension='.ck',
                                             filetypes=(('ck files', '*.ck'), ("all files", "*.*")))
        with open('log.ck', 'r') as file:
            try:
                file_name.write(file.read())
            except AttributeError:
                return

    def save_change_party(self, party):
        for line in fileinput.input('log.ck', inplace=1):
            if line.find("human") != -1:
                line = line.replace(line, 'human:' + party + '\n')
            sys.stdout.write(line)

    def change_fild_text(self, dimension, field):
        filed_in_str = ""
        for i in range(0, dimension):
            for j in range(0, dimension):
                symbol = '0'
                if type(field[i][j]) == game_logic.Chip:
                    if field[i][j].party == 'white':
                        symbol = 1
                        if field[i][j].unusual_checker:
                            symbol = 3
                        if field[i][j].is_king:
                            symbol = 5
                    else:
                        symbol = 2
                        if field[i][j].is_king:
                            symbol = 6
                        if field[i][j].unusual_checker:
                            symbol = 4
                filed_in_str += str(symbol)
            filed_in_str += '\n'
        with open('log.ck', 'a') as file:
            file.write('relise:' + str(self.count_write)+'\n')
            file.write(filed_in_str)
            self.count_write += 1

    def create_struct_log(self, party, dimension, progress):
        with open('log.ck', 'w') as file:
            self.dimension = dimension
            mode = "coop"
            human_party = 'none'
            if party is not None:
                mode = "single"
                human_party = party
            file.write('mode:' + mode + '\n')
            file.write('human:' + human_party + '\n')
            file.write('dimension:' + str(dimension) + '\n')

    def get_field(self):
        res = []
        last_field = 0
        with open(self.log_name, 'r') as file:
            all_line = file.readlines()
        for i in range(0, len(all_line)):
            if all_line[i].find('relise') != -1:
                last_field = i
        for i in range(last_field + 1, self.dimension + last_field + 1):
            res.append([all_line[i][j] for j in range(0, len(all_line[i]) - 1)])
        return res

    def get_is_human(self):
        with open(self.log_name, 'r') as file:
            all_line = file.readlines()
        for line in all_line:
            if line.find('human:') != -1:
                return line[6:-1]

    def get_progress(self):
        return int(self.get_relise())

    def get_dimension(self):
        with open(self.log_name, 'r') as file:
            all_line = file.readlines()
        for line in all_line:
            if line.find('dimension:') != -1:
                return line[10:-1]

    def get_relise(self):
        with open(self.log_name, 'r') as file:
            all_line = file.readlines()
        last_relise = ""
        for line in all_line:
            if line.find('relise') != -1:
                last_relise = line
        return last_relise[7:-1]


if __name__ == "__main__":
    pass
