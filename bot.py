import random


class Bot():

    def __init__(self, player):
        self.player = player
        self.bot_mode = True;

    def find_chip(self):
        if len(self.player.chips_for_fight) > 0:
            index = random.randint(0, len(self.player.chips_for_fight) - 1)
            return self.player.chips_for_fight[index]
        index = random.randint(0, len(self.player.player_chips) - 1)
        return self.player.player_chips[index]

    def take(self):
        self.player.chips_for_fight.clear()
        self.player.analyze_game()
        chip = self.find_chip()
        self.player.take_chip(chip.pos_x, chip.pos_y)

    def find_target(self):
        x = -1
        if (self.player.party == 'white'):
            x = 1
        target_is_find = False
        set_coord = []
        while not target_is_find:
            for y in range(-1, 2):
                pos_x = self.player.active_chip.pos_x + x
                pos_y = self.player.active_chip.pos_y + y
                if abs(x) == abs(y) and self.player.is_correctness_coord(pos_x, pos_y):
                    if type(self.player.field[pos_x][pos_y]) == int:
                        set_coord.append((pos_x, pos_y))
            if len(set_coord) > 0:
                target_is_find = True
            else:
                self.take()
        index = random.randint(0, len(set_coord) - 1)
        return set_coord[index]

    def do_jump(self):
        if len(self.player.active_chip.chips_for_fight) > 0:
            list_target = list(self.player.active_chip.chips_for_fight.keys())
            index = random.randint(0, len(list_target) - 1)
            return self.player.make_jump(list_target[index][0], list_target[index][1], self.player.party)
        target = self.find_target()
        res = self.player.make_jump(target[0], target[1], self.player.party)
        return res

    def bot_do(self):
        self.take()
        res = self.do_jump()
        while self.player.is_block:
            res = self.do_jump()
        return res

