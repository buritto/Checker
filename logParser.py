
import gameLogic
from tkinter import filedialog
import sys


import fileinput


class gameLogParser:

    def __init__(self, log_name):
        self.log_name = log_name
        self.file = None
        self.count_write = 1
        self.dimension = 0

    def close_file(self):
        self.file.close()

    def save_file(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension='.ck', filetypes=(('ck files','*.ck'),("all files","*.*")))
        return_data = open('log.ck', 'r')
        try:
            file.write(return_data.read())
            return_data.close()
            file.close()
        except AttributeError:
            return

    def save_change_party(self, party):
        #self.file = open('log.ck', 'a')
        for line in fileinput.input('log.ck', inplace=1):
            if line.find("human") != -1:
                line = line.replace(line, 'human:' + party + '\n')
            sys.stdout.write(line)


        self.file.close()

    def change_fild_text(self, dimension, field):
        filed_in_str = ""
        for i in range(0, dimension):
            for j in range(0, dimension ):
                symbol = '0'
                if type(field[i][j]) == gameLogic.Chip:
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
        self.file = open('log.ck', 'a')
        self.file.write('relise:' + str(self.count_write)+'\n')
        self.file.write(filed_in_str)
        self.count_write += 1
        self.file.close()

    def create_struct_log(self, party, dimension, progress):
        self.file = open('log.ck', 'w')
        self.dimension = dimension
        mode = "coop"
        human_party = 'none'
        if (party != None):
            mode = "single"
            human_party = party
        self.file.write('mode:' + mode + '\n')
        self.file.write('human:' + human_party + '\n')
        self.file.write('dimension:' + str(dimension)+ '\n')
        self.file.close()

    def get_field(self):
        res = []
        last_field = 0
        file = open(self.log_name, 'r')
        all_line = file.readlines()
        file.close()
        for i in range(0, len(all_line)):
            if all_line[i].find('relise') != -1:
                last_field = i
        for i in range(last_field + 1 , self.dimension + last_field + 1):
            res.append([all_line[i][j] for j in range(0, len(all_line[i]) -1)])
        return res

    def get_is_human(self):
        self.file = open(self.log_name, 'r')
        all_line = self.file.readlines()
        self.file.close()
        for line in all_line:
            if line.find('human:')!= -1:
                return line[6:-1]

    def get_progress(self):
        return int(self.get_relise())

    def get_dimension(self):
        self.file = open(self.log_name, 'r')
        all_line = self.file.readlines()
        self.file.close()
        for line in all_line:
            if line.find('dimension:')!= -1:
                return line[10:-1]

    def get_relise(self):
        file = open(self.log_name, 'r')
        all_line = file.readlines()
        file.close()
        last_relise =""
        for line in all_line:
            if line.find('relise') != -1:
                last_relise = line
        return last_relise[7:-1]


if __name__=="__main__":
    lp = gameLogParser('log.ck')
    lp.create_struct_log('red',10)
    print(lp.get_field())
    print(lp.get_is_human())
    print(lp.get_dimension())