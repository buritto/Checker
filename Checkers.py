
try:
    from tkinter import *
    import game_logic
    import checkers_exception
    from functools import partial
    from tkinter import messagebox
    from tkinter import filedialog
    import log_parser
    import bot
    import argparse
    import time
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(1)


class AdvancedButton(Button):

    def __init__(self, pos_x, pos_y, master=None):
        Button.__init__(self, master)
        self.pos_x = pos_x
        self.pos_y = pos_y


class BasicUsersInterface:

    def check_winner(self):
        res = self.game.initialize_win()
        if res is not None:
            if res == 'first':
                messagebox.showinfo('Message', 'Red won')
            else:
                messagebox.showinfo('Message', 'Blue won')
            return True
        return False

    def draw_correct_move(self, player):
        for i in range(0, len(player.active_chip_list_move)):
            coord = player.active_chip_list_move[i]
            img = PhotoImage(file='image/green.gif')
            self.list_save_image.append(img)
            self.list_button[coord[0]][coord[1]]['image'] = img

    def take_chip(self, x, y):
        try:
            self.draw()
            if self.progress % 2 == 1:
                self.game.first_player.take_chip(x, y)
                self.draw_correct_move(self.game.first_player)
            else:
                self.game.second_player.take_chip(x, y)
                self.draw_correct_move(self.game.second_player)
        except checkers_exception.InvalidTakeChipsException:
            messagebox.showerror('Error', 'Wrong checker is taken')
            return
        except checkers_exception.InvalidEndJump:
            messagebox.showerror('Error', 'Your move is not completed')
            return

    def change_parties(self, player):
        if player.active_chip.unusual_checker:
            if player.active_chip.count > 0:
                player.active_chip.count -= 1
            else:
                messagebox.showinfo("New message", 'Change party !!!!!!')
                player.active_chip.count = 5
                if self.is_with_bot:
                    save_party = self.game.second_player
                    if self.human == 'first':
                        save_party = self.game.first_player
                        self.game.first_player = self.bot.player
                        self.bot.player = save_party
                        self.log.save_change_party('second')
                        return
                    self.game.second_player = self.bot.player
                    self.bot.player = save_party
                    self.log.save_change_party('first')
                    return
                new_party = self.game.second_player
                self.game.second_player = self.game.first_player
                self.game.first_player = new_party

    def bot_do(self):
        self.bot.take()
        res = self.bot.do_jump()
        while self.bot.player.is_block:
            self.draw()
            res = self.bot.do_jump()
            time.sleep(0.7)
            self.draw()
        time.sleep(0.7)
        return res

    def make_jump(self, x, y):
        try:
            if self.progress % 2 == 1:
                result_jump = self.game.first_player.make_jump(x, y, self.game.first_player.party)
                self.progress += result_jump
                self.change_parties(self.game.first_player)
            else:
                result_jump = self.game.second_player.make_jump(x, y, self.game.second_player.party)
                self.progress += result_jump
                self.draw_correct_move(self.second_player)
                self.change_parties(self.game.second_player)
            self.log.change_fild_text(self.dimension, self.game.field)
        except checkers_exception.InvalidJump:
            messagebox.showerror('Error', 'Wrong move')
            return
        except checkers_exception.InvalidJumpAttack:
            messagebox.showerror('Error', 'You must attack your enemy')
            return
        self.draw()
        if result_jump == 0:
            if self.progress % 2 == 1:
                self.draw_correct_move(self.first_player)
            else:
                self.draw_correct_move(self.second_player)
        if self.check_winner():
            self.root.destroy()
            main()
            return

        if result_jump != 0 and self.human is not None and self.bot.bot_mode:
            if self.check_winner():
                self.root.destroy()
                main()
                return
            self.progress += self.bot_do()
            self.change_parties(self.bot.player)
            self.log.change_fild_text(self.dimension, self.game.field)
            self.draw()
            if self.check_winner():
                self.root.destroy()
                main()

    def draw(self):
        for x in range(0, self.game.dimension):
            start_step = 1
            if x % 2 == 1:
                start_step = 0
            for y in range(start_step, self.game.dimension, 2):
                pos_x = x
                pos_y = y
                if type(self.game.field[x][y]) == game_logic.Chip:
                    self.list_button[x][y]['command'] = partial(self.take_chip, pos_x, pos_y)
                    if self.game.field[x][y].party == 'white':
                        if self.game.field[x][y].is_king:
                            img = PhotoImage(file='image/firstK.gif')
                        else:
                            img = PhotoImage(file='image/first.gif')
                    else:
                        if self.game.field[x][y]. is_king:
                            img = PhotoImage(file='image/secondK.gif')
                        else:
                            img = PhotoImage(file='image/second.gif')
                else:
                    self.list_button[x][y]['command'] = partial(self.make_jump, pos_x, pos_y)
                    img = PhotoImage(file='image/black.gif')
                self.list_save_image.append(img)
                self.list_button[x][y]['image'] = img
        self.root.update()

    def save_game(self):
        self.log.save_file()

    def __init__(self, root, party=None, dimension=10, file_path="", unusual_mode=False):
        self.root = root
        if file_path == "":
            self.log = log_parser.GameLogParser('log.ck')
            self.game = game_logic.PlayingField(dimension, None, unusual_mode)
            self.human = party
            self.dimension = dimension
            self.progress = 1
            self.log.create_struct_log(party, self.dimension, self.progress)
        else:
            self.log = log_parser.GameLogParser(file_path)
            self.log.dimension = int(self.log.get_dimension())
            self.dimension = self.log.dimension
            self.progress = self.log.get_progress() + 1
            self.log.count_write = self.progress + 0
            field_save = self.log.get_field()
            self.game = game_logic.PlayingField(self.dimension, field_save)
            if self.log.get_is_human() == 'none':
                self.human = None
                party = None
            else:
                self.human = self.log.get_is_human()
                party = self.human
        self.first_player = self.game.first_player
        self.second_player = self.game.second_player
        self.root = root
        self.list_button = []
        self.list_save_image = []
        for x in range(0, self.game.dimension):
            new_line = []
            for y in range(0, self.game.dimension):
                new_line.append(AdvancedButton(x, y, self.root))
                img = PhotoImage(file='image/white.gif')
                self.list_save_image.append(img)
                new_line[y]['image'] = img
            self.list_button.append(new_line)
        self.is_with_bot = False
        if party is not None:
            self.is_with_bot = True
            if party == 'first':
                self.bot = bot.Bot(self.second_player)
            else:
                self.bot = bot.Bot(self.first_player)
                if self.progress % 2 != 0:
                    self.progress += self.bot_do()
                    self.log.change_fild_text(self.dimension, self.game.field)
        self.draw()
        for x in range(0, self.game.dimension):
            for y in range(0, self.game.dimension):
                self.list_button[x][y].grid(row=x, column=y)
        menu_bar = Menu(self.root)
        menu_bar.add_command(label="Save", command=self.save_game)
        self.root.config(menu=menu_bar)
        self.root.mainloop()


class GameMenu:

    def __init__(self, root):
        self.list_image = []
        self.root = root
        self.draw_menu(self.root)
        self.is_unusual = IntVar()

    def choose_dimension(self):
        self.clear_form(self.root)
        check_is_mod_unusual = Checkbutton(self.root, text=u'starting with unusual mod', variable=self.is_unusual,
                                           onvalue=1, offvalue=0)
        label = Label(self.root, text='Choose dimension')
        entry_dimension = Entry(self.root)
        start_mode_coop = Button(self.root, text='Start game', width=10, height=3,
                                 command=partial(self.start_game, None, self.root,
                                                 entry_dimension))
        entry_dimension.grid(row=0, column=2)
        label.grid(row=0, column=0)
        back = Button(self.root, text='Back', width=5, command=partial(self.draw_menu, self.root))
        back.grid(row=3, column=1, pady=10, padx=0)
        start_mode_coop.grid(row=2, pady=10, padx=8, column=1)
        check_is_mod_unusual.grid(row=1, column=0)

    def start_game(self, party, root, entry):
        dimension = entry.get()
        if len(dimension) == 0:
            self.clear_form(root)
            BasicUsersInterface(root, party, 10, "", self.is_unusual.get())
        else:
            try:
                if int(dimension) < 5 or int(dimension) % 2 == 1:
                    messagebox.showerror('Error dimension',
                                         'Incorrect dimension: dimension should be more 4 and be even ')
                    self.clear_form(self.root)
                    self.draw_menu(self.root)
                    return
                self.clear_form(root)
                BasicUsersInterface(root, party, int(dimension), "", self.is_unusual.get())
            except ValueError:
                messagebox.showerror('Error dimension', 'Set incorrect dimension')
                self.draw_menu(self.root)

    def clear_form(self, root):
        widget_list = root.grid_slaves()
        for widget in widget_list:
            widget.destroy()

    def take_party(self, root):
        self.clear_form(root)
        check_is_mod_unusual = Checkbutton(self.root, text=u'starting with unusual mod', variable=self.is_unusual,
                                           onvalue=1, offvalue=0)
        img_first = PhotoImage(file='image/first.gif')
        self.list_image.append(img_first)
        img_second = PhotoImage(file='image/second.gif')
        self.list_image.append(img_second)
        entry_dimension = Entry(root)
        first_player = Button(root, text='Red', image=img_first, command=partial(self.start_game, 'first',
                                                                                 root, entry_dimension))
        second_player = Button(root, text='Blue', image=img_second, command=partial(self.start_game, 'second',
                                                                                    root, entry_dimension))
        label = Label(root, text='Choose dimension')
        back = Button(root, text='Back', width=5, command=partial(self.draw_menu, root))
        Label(text='Choose party').grid(row=0, column=1, padx=8, pady=20)
        first_player.grid(row=4, column=0, pady=20, padx=8)
        second_player.grid(row=4, column=2, pady=20, padx=8)
        entry_dimension.grid(row=1, column=2)
        label.grid(row=1, column=0)
        back.grid(row=5, column=1, pady=10, padx=8)
        check_is_mod_unusual.grid(row=3, column=0)

    def loading(self):
        open_file_path = filedialog.askopenfilename(title="Select file", defaultextension=".ck",
                                                    filetypes=(('ck files', '*.ck'), ("all files", "*.*")))
        if len(open_file_path) != 0:
            self.start_game_from_file(open_file_path)

    def start_game_from_file(self, file_name):
        self.clear_form(self.root)
        BasicUsersInterface(self.root, file_path=file_name)

    def draw_menu(self, root):
        self.clear_form(root)
        take_mode_single = Button(root, text='Single mode', width=10, height=3, command=partial(self.take_party, root))
        take_mode_coop = Button(root, text='Coop mode', width=10, height=3, command=partial(self.choose_dimension))
        take_louding = Button(root, text='Load save', width=10, height=3, command=partial(self.loading))
        quit = Button(root, text='Quit', width=10, height=3, command=lambda: self.root.destroy())
        canvas = Canvas(height=200, width=300)
        img = PhotoImage(file='image/main.gif')
        self.list_image.append(img)
        canvas.create_image(169, 100, image=img)
        take_mode_single.grid(row=0, pady=10, padx=8)
        take_mode_coop.grid(row=1, pady=10, padx=8)
        take_louding.grid(row=2, pady=10, padx=8)
        quit.grid(row=3, pady=10, padx=8)
        canvas.grid(row=0, rowspan=3, column=1, padx=8)


def main():
    root = Tk()
    menu = GameMenu(root)
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load", metavar="path", help="load game from file", type=str)
    parser.add_argument("-m", "--multi", metavar="dimension", help="start multiplayer game with dimension", type=int)
    parser.add_argument("-s", "--singleplayer", metavar=("party", "dimension"), help="start singlplayer",
                        nargs=2, type=int)
    args = parser.parse_args()
    if args.load:
        path_file = args.load
        if path_file.split('.')[-1] != 'ck':
            raise checkers_exception.InvalidPathToFileLoad
        menu.start_game_from_file(path_file)
    if args.multi:
        if args.multi % 2 != 0 or args.multi <= 4:
            raise checkers_exception.InvalidDimension()
        menu.clear_form(root)
        BasicUsersInterface(root, None, args.multi)
    if args.singleplayer:
        if args.singleplayer[1] % 2 != 0 or args.singleplayer[1] <= 4:
            raise checkers_exception.InvalidDimension()
        if args.singleplayer[0] != 1 and args.singleplayer[0] != 2:
            raise checkers_exception.InvalidParty
        party = 'first'
        if args.singleplayer[0] == 2:
            party = 'second'
        menu.clear_form(root)
        BasicUsersInterface(root, party, args.singleplayer[1])
    root.mainloop()


if __name__ == "__main__":
    main()
