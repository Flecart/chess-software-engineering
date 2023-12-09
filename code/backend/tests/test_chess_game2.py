import asyncio
import unittest
from unittest.mock import patch, MagicMock
from backend.game.v1_chess_game import ChessGame, Color, CreateGameRequest
from backend.game.utils import START_POSITION_FEN

class TestChessGameMethods(unittest.TestCase):
    def setUp(self):
        self.game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        self.chess_game = ChessGame(self.game_request)

    def test_id(self):
        self.assertEqual(self.chess_game.id, self.chess_game._ChessGame__id)

    def test_fen(self):
        self.assertEqual(self.chess_game.fen, START_POSITION_FEN)

    def test_moves(self):
        self.assertEqual(self.chess_game.moves, [])

    def test_white_view(self):
        self.assertEqual(self.chess_game.white_view, self.chess_game._ChessGame__white_view)

    def test_black_view(self):
        self.assertEqual(self.chess_game.black_view, self.chess_game._ChessGame__black_view)

    def test_current_player(self):
        self.assertEqual(self.chess_game.current_player, Color.WHITE)

    def test_is_current_player(self):
        self.chess_game.join("user1", Color.WHITE)
        self.assertTrue(self.chess_game.is_current_player("user1"))
        self.assertFalse(self.chess_game.is_current_player("user2"))

    def test_join(self):
        self.chess_game.join("user1", Color.WHITE)
        self.assertEqual(self.chess_game._ChessGame__white_player, "user1")
        self.chess_game.join("user2", Color.BLACK)
        self.assertEqual(self.chess_game._ChessGame__black_player, "user2")

    def test_get_player_color(self):
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        self.assertEqual(self.chess_game.get_player_color("user1"), Color.WHITE)
        self.assertEqual(self.chess_game.get_player_color("user2"), Color.BLACK)

    def test_get_moves(self):
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        self.assertIsNotNone(self.chess_game.get_moves())

    def test_get_best_move(self):
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        self.assertIsNotNone(self.chess_game.get_best_move())

    def test_get_working_move(self):
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        self.assertIsNotNone(self.chess_game.get_working_move())

    def test_move(self):
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        move = self.chess_game.get_best_move()
        self.assertIsNotNone(self.chess_game.move(move))
        move = self.chess_game.get_best_move()
        self.assertIsNotNone(self.chess_game.move(move))
        move = self.chess_game.get_best_move()
        self.assertIsNotNone(self.chess_game.move(move))

    @patch('backend.game.v1_chess_game.engine')
    def test_move_finished_game(self, mock_engine):
        # Set up the game so that it's finished
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        self.chess_game._ChessGame__finished = True

        # Try to make a move
        move = "e2e4"
        result = self.chess_game.move(move)

        # Check that the move was not made
        self.assertIsNone(result)

        # Check that the engine was not called
        mock_engine.dispatch.assert_not_called()
    
    @patch('backend.game.v1_socket_manager.SocketManager')
    def test_get_bot_move(self, mock_socket_manager):
        self.game_request = CreateGameRequest(type="dark_chess", against_bot=True, time=10)
        self.chess_game = ChessGame(self.game_request)

        # Set up the game so that the bot should make a move
        self.chess_game.join("user1", Color.BLACK)

        # Mock the event loop
        event_loop = asyncio.new_event_loop()

        # Call get_bot_move
        self.chess_game.get_bot_move(event_loop)

        # Check that the bot made a move
        # self.assertNotEqual(self.chess_game.fen, START_POSITION_FEN)

        # Check that the bot notified the opponent
        # mock_socket_manager.assert_called_once()

if __name__ == "__main__":
    unittest.main()