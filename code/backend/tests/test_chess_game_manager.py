import unittest
from unittest.mock import patch, MagicMock

from backend.game.v1_chess_game_manager import ChessGameManager
from backend.game.v1_chess_game import ChessGame, Color, CreateGameRequest


class TestChessGameManager(unittest.TestCase):
    def setUp(self):
        self.manager = ChessGameManager()
        self.game_request = CreateGameRequest(
            type="dark_chess", against_bot=False, time=10
        )

    def tearDown(self):
        self.manager._instance = None

    def test_singleton(self):
        manager2 = ChessGameManager()
        self.assertEqual(self.manager, manager2)

    def test_create_new_game(self):
        game_id = self.manager.create_new_game(self.game_request)
        self.assertIsInstance(self.manager.get_game(game_id), ChessGame)

    def test_join(self):
        game_id = self.manager.create_new_game(self.game_request)
        self.manager.join(game_id, 0, Color.WHITE)
        with self.assertRaises(ValueError):
            self.manager.join(game_id, 0, Color.WHITE)
        self.manager.join(game_id, 1, Color.BLACK)
        with self.assertRaises(ValueError):
            self.manager.join(game_id, 1, Color.BLACK)

    @patch.object(ChessGame, "move")
    def test_move(self, mock_move):
        game_id = self.manager.create_new_game(self.game_request)
        self.manager.join(game_id, 2, Color.WHITE)
        self.manager.join(game_id, 3, Color.BLACK)
        self.manager.move(game_id, 2, "e2e4")
        mock_move.assert_called_once_with("e2e4")

    def test_get_view(self):
        game_id = self.manager.create_new_game(self.game_request)
        self.manager.join(game_id, 4, Color.WHITE)
        self.manager.join(game_id, 5, Color.BLACK)
        self.assertIsInstance(self.manager.get_view(game_id, Color.WHITE), str)
        self.assertIsInstance(self.manager.get_view(game_id, Color.BLACK), str)

    def test_get_moves(self):
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        game_id = self.manager.create_new_game(game_request)
        self.manager.join(game_id, 1, Color.WHITE)
        self.manager.join(game_id, 2, Color.BLACK)
        self.assertIsInstance(self.manager.get_moves(game_id), list)
