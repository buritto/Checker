import game_logic
import unittest
import checkers_exception
import log_parser
import glob
import os


class ParserTest(unittest.TestCase):
    file_for_deleted = []

    def tearDown(self):
        for file in self.file_for_deleted:
            os.remove(file)

    def init_parser(self):
        self.parse = log_parser.GameLogParser("log.ck")

    def test_created_log(self):
        new_parser = log_parser.GameLogParser("log.ck")
        new_parser.create_struct_log("white", 10, 1)
        os.chdir(os.getcwd())
        files = []
        for file in glob.glob("*.ck"):
            files.append(file)
        self.file_for_deleted.append('log.ck')
        self.assertTrue("log.ck" in files)

    def test_save_field(self):
        expected = ["010101\n",
                    "101010\n",
                    "000000\n",
                    "000000\n",
                    "020202\n",
                    "202020\n", ]
        new_game = game_logic.PlayingField(6)
        new_parser = log_parser.GameLogParser("log.ck")
        new_parser.create_struct_log("", 6, 1)
        new_parser.change_fild_text(6, new_game.field)
        with open("log.ck", 'r') as file:
            all_lines = file.readlines()
            actual = all_lines[4:]
            self.assertEqual(expected, actual)

    def init_players(self):
        self.new_game = game_logic.PlayingField(6)
        self.white = self.new_game.first_player
        self.black = self.new_game.second_player

    def test_get_field(self):
        expected = [['0', '1', '0', '1', '0', '1'],
                    ['1', '0', '1', '0', '0', '0'],
                    ['0', '0', '0', '0', '0', '1'],
                    ['2', '0', '0', '0', '0', '0'],
                    ['0', '0', '0', '2', '0', '2'],
                    ['2', '0', '2', '0', '2', '0'],
                    ]
        self.init_players()
        new_parser = log_parser.GameLogParser("log.ck")
        new_parser.create_struct_log("", 6, 1)
        self.white.take_chip(1, 4)
        self.white.make_jump(2, 5, 'white')
        new_parser.change_fild_text(6, self.new_game.field)
        self.black.take_chip(4, 1)
        self.black.make_jump(3, 0, 'black')
        new_parser.change_fild_text(6, self.new_game.field)
        field = new_parser.get_field()
        self.assertEqual(expected, field)

    def test_get_is_human(self):
        self.init_players()
        new_parser = log_parser.GameLogParser("log.ck")
        new_parser.create_struct_log("white", 6, 1)
        self.assertEqual('white', new_parser.get_is_human())
        new_parser.create_struct_log("black", 6, 1)
        self.assertEqual('black', new_parser.get_is_human())

    def test_get_progress(self):
        self.init_players()
        new_parser = log_parser.GameLogParser("log.ck")
        new_parser.create_struct_log("", 6, 1)
        self.white.take_chip(1, 4)
        self.white.make_jump(2, 5, 'white')
        new_parser.change_fild_text(6, self.new_game.field)
        self.black.take_chip(4, 1)
        self.black.make_jump(3, 0, 'black')
        new_parser.change_fild_text(6, self.new_game.field)
        self.assertEqual(2, int(new_parser.get_relise()))

    def test_get_dimension(self):
        new_parser = log_parser.GameLogParser("log.ck")
        new_parser.create_struct_log("", 6, 1)
        self.assertEqual(6, int(new_parser.get_dimension()))

    def test_save_party(self):
        name_party = "MY_PARTY"
        new_parser = log_parser.GameLogParser("log.ck")
        new_parser.create_struct_log("", 6, 1)
        new_parser.save_change_party(name_party)
        self.assertEqual(name_party, new_parser.get_is_human())


class LogicTest(unittest.TestCase):
    game = game_logic.PlayingField(10)
    white = game.first_player
    black = game.second_player

    def init_king(self, pos_x, pos_y):
        for x in range(0, 10):
            for y in range(0, 10):
                self.game.field[x][y] = 0
        self.game.field[pos_x][pos_y] = game_logic.Chip(pos_x, pos_y, 'black', self.white, False)
        self.white.player_chips.append(self.game.field[pos_x][pos_y])

    def init_data(self):
        self.game = game_logic.PlayingField(10)
        self.white = self.game.first_player
        self.black = self.game.second_player

    def test_correct_init_player(self):
        game = game_logic.PlayingField(10)
        white = game_logic.Player('white', game.field)
        game.put_chips(0, 1, 0, 9, 'black', white, False)
        self.assertEqual(len(white.player_chips), 5)

    def test_correct_move(self):
        self.init_data()
        self.white.take_chip(3, 0)
        self.white.make_jump(4, 1, 'white')
        self.assertEqual(self.game.field[3][0], 0)
        self.assertTrue(type(self.game.field[4][1]) == game_logic.Chip)

    def print_game_state(self):
        for x in range(0, 10):
            my_list = []
            for y in range(0, 10):
                if type(self.game.field[x][y]) == game_logic.Chip:
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

    def test_is_king(self):
        game = game_logic.PlayingField(6)
        game.first_player.field[5][0] = game_logic.Chip(5, 0, 'second', game.first_player, False)
        game.first_player.it_chip_is_king(game.first_player.field[5][0])
        self.assertTrue(game.first_player.field[5][0].is_king)

    def test_king_fight(self):
        self.init_king(8, 5)
        self.white.take_chip(8, 5)
        self.white.make_jump(9, 6, 'white')
        chip_enemy = game_logic.Chip(4, 1, 'white', self.black, False)
        self.game.field[4][1] = chip_enemy
        self.black.player_chips.append(chip_enemy)
        self.white.take_chip(9, 6)
        self.assertTrue((3, 0) in self.white.active_chip.chips_for_fight)
        self.white.make_jump(3, 0, 'white')
        self.assertEqual(self.game.field[4][1], 0)

    def test_incorrect_take(self):
        self.init_data()
        with self.assertRaises(checkers_exception.InvalidTakeChipsException):
            self.black.take_chip(5, 0)

    def test_incorrect_jump(self):
        self.init_data()
        self.black.take_chip(6, 1)
        with self.assertRaises(checkers_exception.InvalidJump):
            self.black.make_jump(5, 1, 'black')

    def test_init_winner(self):
        game = game_logic.PlayingField(6)
        game.first_player.player_chips = []
        self.assertEqual('second', game.initialize_win())

    def test_blocked_analyze(self):
        game = game_logic.PlayingField(6)
        for x in range(0, game.dimension):
            for y in range(0, game.dimension):
                game.field[x][y] = game_logic.Chip(x, y, 'second', game.first_player, False)
        self.assertEqual(0, game.analyze_locks(game.first_player))

    def test_checker_correct_coord(self):
        game = game_logic.PlayingField(6)
        self.assertTrue(game.first_player.is_correctness_coord(3, 3))
        self.assertFalse(game.first_player.is_correctness_coord(100500, -100500))

    def test_correct_step_for_chip(self):
        game = game_logic.PlayingField(100)
        self.assertEqual([1], game.first_player.get_step_list(game.field[0][1]))


if __name__ == "__main__":
    unittest.main()
