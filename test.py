import gameLogic
import unittest
import checkersException


class LogicTest(unittest.TestCase):
    game = gameLogic .PlayingField(10)
    white = game.first_player
    black = game.second_player

    def init_king(self, pos_x, pos_y):
        for x in range(0, 10):
            for y in range(0, 10):
                self.game.field[x][y] = 0
        self.game.field[pos_x][pos_y] = gameLogic.Chip(pos_x, pos_y, 'black', self.white, False)
        self.white.player_chips.append(self.game.field[pos_x][pos_y])

    def init_data(self):
        self.game = gameLogic.PlayingField(10)
        self.white = self.game.first_player
        self.black = self.game.second_player

    def test_correct_move(self):
        self.init_data()
        self.white.take_chip(3, 0)
        self.white.make_jump(4, 1, 'white')
        self.assertEqual(self.game.field[3][0], 0)
        self.assertTrue(type(self.game.field[4][1]) == gameLogic.Chip)



    def print_game_state(self):
        for x in range(0, 10):
            my_list = []
            for y in range(0, 10):
                if type(self.game.field[x][y]) == gameLogic.Chip:
                    if self.game.field[x][y].party == 'black':
                        my_list.append('b')
                    else:
                        my_list.append('w')
                else:
                    my_list.append('-')
            print(str(my_list))

    def test_big_fight(self):
        self.init_data()
        count_white_before_battle = len(self.white.player_chips)
        for y in range(0, 10, 2):
            self.white.take_chip(3, y)
            self.white.make_jump(4, y + 1, 'white')
        self.black.take_chip(6, 1)
        self.black.make_jump(5, 0, 'black')
        self.black.take_chip(5, 0)
        for i in range(0, 2):
            self.black.make_jump(self.black.active_chip.pos_x - 2, self.black.active_chip.pos_y + 2, 'black')
            self.black.make_jump(self.black.active_chip.pos_x + 2, self.black.active_chip.pos_y + 2, 'black')
        self.assertEqual(len(self.white.player_chips), count_white_before_battle - 4)

    def test_king_jump(self):
        self.init_king(8, 5)
        self.white.take_chip(8, 5)
        self.white.make_jump(9, 6, 'white')
        self.assertTrue(self.white.active_chip.is_king)

    def test_king_fight(self):
        self.init_king(8, 5)
        self.white.take_chip(8, 5)
        self.white.make_jump(9, 6, 'white')
        chip_enemy = gameLogic.Chip(4, 1, 'white', self.black, False)
        self.game.field[4][1] = chip_enemy
        self.black.player_chips.append(chip_enemy)
        self.white.take_chip(9, 6)
        self.assertTrue((3, 0) in self.white.active_chip.chips_for_fight)
        self.white.make_jump(3, 0, 'white')
        self.assertEqual(self.game.field[4][1], 0)

    def test_incorrect_take(self):
        self.init_data()
        with self.assertRaises(checkersException.InvalidTakeChipsException):
            self.black.take_chip(5, 0)

    def test_incorrect_jump(self):
        self.init_data()
        self.black.take_chip(6, 1)
        with self.assertRaises(checkersException.InvalidJump):
            self.black.make_jump(5, 1, 'black')
    suite = unittest.TestSuite()
    suite.addTest(test_correct_move)
    suite.addTest(test_big_fight)
    suite.addTest(test_king_jump)
    suite.addTest(test_king_fight)
    suite.addTest(test_incorrect_take)
    suite.addTest(test_incorrect_jump)

