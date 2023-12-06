import unittest

from backend.bot.data.game_state_input import GameStateInput
from backend.bot.data.game_state_output import GameStateOutput
from backend.bot.data.enums import GameType, Actions
from backend.bot.mcts import dispatch


class TestMCTS(unittest.TestCase):
    def setUp(self):
        self.game = GameStateInput(GameType.DARK_CHESS, "", [], None)
        self.game.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def test_initialisation(self):
        self.assertEqual(
            self.game.fen, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )
        self.assertEqual(self.game.game_type, GameType.DARK_CHESS)

        with self.subTest("Test mosse valide all'appertura"):
            self.game.action = Actions.LIST_MOVE
            val = dispatch(self.game)
            self.assertEqual(
                val.possible_moves,
                [
                    "a2a3",
                    "a2a4",
                    "b1a3",
                    "b1c3",
                    "b2b3",
                    "b2b4",
                    "c2c3",
                    "c2c4",
                    "d2d3",
                    "d2d4",
                    "e2e3",
                    "e2e4",
                    "f2f3",
                    "f2f4",
                    "g1f3",
                    "g1h3",
                    "g2g3",
                    "g2g4",
                    "h2h3",
                    "h2h4",
                ],
            )  # all possible opening moves

        with self.subTest("Test mosse fen"):
            self.game.move = "d2d4"  # two valid moves
            self.game.action = Actions.MOVE
            val = dispatch(self.game)

            self.game.fen = val.fen
            self.assertEqual(
                self.game.fen,
                "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1",
            )

            self.game.move = "d7d5"
            self.game.action = Actions.MOVE
            val = dispatch(self.game)

            self.game.fen = val.fen
            self.assertEqual(
                self.game.fen,
                "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 2",
            )

        with self.subTest("Test mossa invalida (Re volante)"):
            self.game.move = "e1e8"
            self.game.action = Actions.MOVE

            with self.assertRaises(ValueError):
                val = dispatch(self.game)

        # L'engine restiture una lista di mosse vuota se mancano i re sulla board


class TestPiecesMoves(unittest.TestCase):
    def setUp(self):
        self.game = GameStateInput(GameType.DARK_CHESS, "", [], None)

    def test_Pawn(self):
        self.game.fen = "7k/p7/1P6/8/8/7P/8/7K b - - 2 3"
        self.game.action = Actions.LIST_MOVE
        val = dispatch(self.game)
        self.assertEqual(
            val.possible_moves, ["a7a6", "a7a5", "a7b6", "h8h7", "h8g8", "h8g7"]
        )

    def test_Rook(self):
        self.game.fen = "7k/8/8/3R4/8/8/8/7K w - - 4 20"
        self.game.action = Actions.LIST_MOVE
        val = dispatch(self.game)
        self.assertEqual(
            val.possible_moves,
            [
                "d5d1",
                "d5d2",
                "d5d3",
                "d5d4",
                "d5d6",
                "d5d7",
                "d5d8",
                "d5a5",
                "d5b5",
                "d5c5",
                "d5e5",
                "d5f5",
                "d5g5",
                "d5h5",
                "h1h2",
                "h1g1",
                "h1g2",
            ],
        )  # full cross

        self.game.fen = "7k/8/8/1p1R4/8/3P4/8/7K w - - 4 20"
        self.game.action = Actions.LIST_MOVE
        val = dispatch(self.game)
        self.assertEqual(
            val.possible_moves,
            [
                "d3d4",
                "d5d4",
                "d5d6",
                "d5d7",
                "d5d8",
                "d5b5",
                "d5c5",
                "d5e5",
                "d5f5",
                "d5g5",
                "d5h5",
                "h1h2",
                "h1g1",
                "h1g2",
            ],
        )  # cross \w enemy e ally

    def test_Knight(self):
        self.game.fen = "7k/8/8/3N4/8/8/8/7K w - - 4 20"
        self.game.action = Actions.LIST_MOVE
        val = dispatch(self.game)
        self.assertEqual(
            val.possible_moves,
            [
                "d5b4",
                "d5b6",
                "d5c3",
                "d5c7",
                "d5f4",
                "d5f6",
                "d5e3",
                "d5e7",
                "h1h2",
                "h1g1",
                "h1g2",
            ],
        )

        knight_moves0 = val.possible_moves

        self.game.fen = "7k/8/3pp3/3N4/1n6/2P5/8/7K w - - 4 20"
        self.game.action = Actions.LIST_MOVE

        # knight_moves1 = [ x for x in knight_moves0 if x != 'd5c3'] + ['c3c4','c3b4'] # TODO ???
        # val = dispatch(self.game)
        # self.assertEqual(val.possible_moves,knight_moves1)


class TestSpecialSituation(unittest.TestCase):  # TODO pensare ad un nome migliore
    def setUp(self):
        self.game = GameStateInput(GameType.DARK_CHESS, "", [], None)

    def test_check(self):
        game = self.game

        with self.subTest("Avaliable moves in check (CHESS mode)"):
            game.game_type = GameType.CHESS
            game.fen = "7k/7q/8/8/8/8/8/6PK w - - 3 5"
            game.action = Actions.LIST_MOVE

            val = dispatch(game)
            self.assertEqual(val.possible_moves, ["h1g2"])

        with self.subTest("Best move in check position"):
            game.game_type = GameType.DARK_CHESS
            game.fen = "k7/8/8/8/8/6n1/6PR/7K w - - 0 1"
            game.action = Actions.MAKE_BEST_MOVE

            val = dispatch(game)
            # print(f'FEN: {val.fen}')
            # print(f'white_view: {val.white_view}')
            # print(f'black_view: {val.black_view}')
            self.assertEqual(val.best_move, "h1g1")

        with self.subTest("King capturable"):
            game.fen = "k7/8/8/8/8/6n1/6PR/7K b - - 0 1"
            game.action = Actions.LIST_MOVE

            val = dispatch(game)

            if val.possible_moves is not None:
                self.assertIn("g3h1", val.possible_moves)

    def test_enpassant(self):
        game = self.game

        game.game_type = GameType.DARK_CHESS
        game.fen = "7k/8/8/8/4p3/8/3P4/K7 w - - 0 1"
        game.action = Actions.MOVE
        game.move = "d2d4"

        val = dispatch(game)
        self.assertEqual("7k/8/8/8/3Pp3/8/8/K7 b - d3 0 1", val.fen)
        game.fen = val.fen

        game.action = Actions.LIST_MOVE
        val = dispatch(game)
        if val.possible_moves is not None:
            self.assertIn("e4d3", val.possible_moves)

        game.action = Actions.MOVE
        game.move = "e4d3"

        val = dispatch(game)
        self.assertEqual("7k/8/8/8/8/3p4/8/K7 w - - 0 2", val.fen)

    def test_castle(self):
        game = self.game

        game.game_type = GameType.DARK_CHESS
        game.fen = "k7/8/8/8/8/8/8/R3K2R w KQ - 0 1"
        game.action = Actions.LIST_MOVE

        val = dispatch(game)

        if val.possible_moves is not None:
            self.assertIn("e1c1", val.possible_moves)
            self.assertIn("e1g1", val.possible_moves)

        with self.subTest("Queen Side Castle"):
            game.action = Actions.MOVE  # Queen Side
            game.move = "e1c1"

            val = dispatch(game)
            self.assertEqual("k7/8/8/8/8/8/8/2KR3R b - - 1 1", val.fen)

        with self.subTest("King Side Castle"):
            game.action = Actions.MOVE  # King Side
            game.move = "e1g1"

            val = dispatch(game)
            self.assertEqual("k7/8/8/8/8/8/8/R4RK1 b - - 1 1", val.fen)

        # game.fen = 'k4r2/8/8/8/8/8/8/R3K2R w Q - 0 1'
        # game.action = Actions.LIST_MOVE
        #
        # val = dispatch(game)
        # print(val.possible_moves)

    def test_promotion(self):
        game = self.game
        game.game_type = GameType.DARK_CHESS
        game.fen = "k7/3P4/8/8/8/8/8/7K w - - 0 1"

        game.action = Actions.LIST_MOVE
        val = dispatch(game)
        self.assertEqual(
            ["d7d8r", "d7d8b", "d7d8n", "d7d8q", "h1h2", "h1g1", "h1g2"],
            val.possible_moves,
        )

        game.action = Actions.MOVE
        game.move = "d7d8n"

        val = dispatch(game)
        self.assertEqual("k2N4/8/8/8/8/8/8/7K b - - 0 1", val.fen)


class TestFogOfWar(unittest.TestCase):
    def setUp(self):
        self.game = GameStateInput(GameType.DARK_CHESS, "", [], None)

    def test_openingFogOfWar(self):
        game = self.game

        game.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"

        game.action = Actions.LIST_MOVE
        val = dispatch(game)

        with self.subTest("Black fog of war"):
            self.assertEqual(
                "rnbqkbnr/pppppppp/8/8/????????/????????/????????/???????? w - - 0 1",
                val.black_view,
            )

        with self.subTest("White fog of war"):
            self.assertEqual(
                "????????/????????/????????/????????/8/8/PPPPPPPP/RNBQKBNR w - - 0 1",
                val.white_view,
            )
