import unittest
from unittest.mock import patch, MagicMock
from backend.bot.data.game_state_output import GameStateOutput
from backend.game.v1_chess_game import ChessGame, Color, CreateGameRequest
from backend.game.utils import START_POSITION_FEN
from backend.game import utils
import asyncio

starting_white_view = (
    "????????/????????/????????/????????/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1"
)
starting_black_view = (
    "rnbqkbnr/pppppppp/8/8/????????/????????/????????/???????? w kq - 0 1"
)

intial_possible_moves = [
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
]

after_e2e4_possible_moves = [
    "a7a6",
    "a7a5",
    "b8a6",
    "b8c6",
    "b7b6",
    "b7b5",
    "c7c6",
    "c7c5",
    "d7d6",
    "d7d5",
    "e7e6",
    "e7e5",
    "f7f6",
    "f7f5",
    "g8f6",
    "g8h6",
    "g7g6",
    "g7g5",
    "h7h6",
    "h7h5",
]


class TestChessGame(unittest.TestCase):
    def test_fen(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        self.assertEqual(chess_game.fen, START_POSITION_FEN)

    def test_moves(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        self.assertEqual(chess_game.moves, [])

    def test_black_view(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        self.assertEqual(chess_game.black_view, starting_black_view)

    def test_white_view(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        self.assertEqual(chess_game.white_view, starting_white_view)

    def test_current_player(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        self.assertEqual(chess_game.current_player, Color.WHITE)

    def test_is_current_player(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.WHITE)
        chess_game.join("user2", Color.BLACK)
        self.assertTrue(chess_game.is_current_player("user1"))
        self.assertFalse(chess_game.is_current_player("user2"))
        chess_game.move("e2e4")
        self.assertFalse(chess_game.is_current_player("user1"))
        self.assertTrue(chess_game.is_current_player("user2"))

    @patch("backend.game.v1_chess_game.get_db_without_close")
    def test_chess_game_join(self, mock_get_db):
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        with self.assertRaises(ValueError):
            chess_game.join("user1", "red")

        chess_game.join("user1", Color.WHITE)
        self.assertEqual(chess_game._ChessGame__white_player, "user1")
        chess_game.join("user2", Color.BLACK)
        self.assertEqual(chess_game._ChessGame__black_player, "user2")
        with self.assertRaises(ValueError):
            chess_game.join("user3", Color.WHITE)
        with self.assertRaises(ValueError):
            chess_game.join("user4", Color.BLACK)

    def test_join_bot_as_black(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=True, time=10)
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.WHITE)
        self.assertEqual(chess_game._ChessGame__white_player, "user1")
        self.assertEqual(chess_game._ChessGame__black_player, "check_mates_bot")

    def test_join_bot_as_white(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=True, time=10)
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.BLACK)
        self.assertEqual(chess_game._ChessGame__black_player, "user1")
        self.assertEqual(chess_game._ChessGame__white_player, "check_mates_bot")

    def test_chess_game_get_player_color(self):
        game_request = CreateGameRequest(
            type="dark_chess", against_bot=False, time=10000
        )
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.WHITE)
        chess_game.join("user2", Color.BLACK)
        self.assertEqual(chess_game.get_player_color("user1"), Color.WHITE)
        self.assertEqual(chess_game.get_player_color("user2"), Color.BLACK)
        self.assertIsNone(chess_game.get_player_color("user3"))

    def test_get_moves(self):
        # returns every possible move
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=0)
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.WHITE)
        chess_game.join("user2", Color.BLACK)
        self.assertEqual(chess_game.get_moves(), intial_possible_moves)
        chess_game.move("e2e4")
        self.assertEqual(chess_game.get_moves(), after_e2e4_possible_moves)
        chess_game.get_best_move()
        chess_game.get_player_response(Color.BLACK)
        chess_game.get_player_response(Color.WHITE)

        chess_game.get_bot_move(asyncio.get_event_loop())

    @unittest.skip("TODO: fix this test")
    @patch("backend.game.v1_chess_game.engine")
    def test_move_valid(self, mock_engine):
        mock_engine.dispatch.return_value = GameStateOutput(
            fen="new_fen",
            black_view="new_black_view",
            white_view="new_white_view",
            general_message="",
            finish=False,
        )
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.WHITE)
        chess_game.join("user2", Color.BLACK)
        message = chess_game.move("e2e4")
        self.assertEqual(message, "")
        self.assertEqual(chess_game.fen, "new_fen")
        self.assertEqual(chess_game.black_view, "new_black_view")
        self.assertEqual(chess_game.white_view, "new_white_view")
        self.assertEqual(chess_game.moves, ["e2e4"])

    @unittest.skip("TODO: fix this test")
    @patch("backend.game.v1_chess_game.engine")
    def test_move_invalid(self, mock_engine):
        mock_engine.dispatch.return_value = GameStateOutput(
            fen="old_fen",
            black_view="old_black_view",
            white_view="old_white_view",
            general_message=utils.KRIEGSPIEL_INVALID_MOVE,
            finish=False,
        )
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.WHITE)
        chess_game.join("user2", Color.BLACK)
        message = chess_game.move("e2e5")
        self.assertEqual(message, utils.KRIEGSPIEL_INVALID_MOVE)
        self.assertEqual(chess_game.fen, "old_fen")
        self.assertEqual(chess_game.black_view, "old_black_view")
        self.assertEqual(chess_game.white_view, "old_white_view")
        self.assertEqual(chess_game.moves, [])

    @unittest.skip("TODO: fix this test")
    @patch("backend.game.v1_chess_game.engine")
    def test_move_finishes_game(self, mock_engine):
        mock_engine.dispatch.return_value = GameStateOutput(
            fen="final_fen",
            black_view="final_black_view",
            white_view="final_white_view",
            general_message="",
            finish=True,
        )
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        chess_game = ChessGame(game_request)
        chess_game.join("user1", Color.WHITE)
        chess_game.join("user2", Color.BLACK)
        message = chess_game.move("e2e4")
        self.assertEqual(message, "")
        self.assertTrue(chess_game.finished)
        self.assertEqual(chess_game.fen, "final_fen")
        self.assertEqual(chess_game.black_view, "final_black_view")
        self.assertEqual(chess_game.white_view, "final_white_view")
        self.assertEqual(chess_game.moves, ["e2e4"])
