import asyncio
import unittest
from unittest.mock import patch, MagicMock
from backend.database.models import Game, User
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
    @patch("backend.game.v1_chess_game.ChessGame.save_and_update_elo")
    @patch("backend.game.v1_chess_game.ChessGame._check_times_up", return_value=True)
    def test_move_finished_game(self, mock_engine, mock_update_elo, mock_check_times_up):
        # Set up the game so that it's finished
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        self.chess_game.__finished = True

        # Try to make a move
        move = "e2e4"
        self.chess_game.move(move)

        # Check that the move was not made
        # self.assertIsNone(result)

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

    @patch('backend.game.v1_chess_game.get_db_without_close')
    @patch("backend.game.v1_chess_game.ChessGame._check_times_up", return_value=True)
    def test_save_and_update_elo(self, mock_get_db, mock_check_times_up):
        # Set up the game so that it's finished
        self.chess_game.join("user1", Color.WHITE)
        self.chess_game.join("user2", Color.BLACK)
        self.chess_game._ChessGame__current_player = Color.BLACK

        # Mock the database session
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock the Game and User objects
        mock_game = MagicMock(spec=Game)
        mock_white_user = MagicMock(spec=User)
        mock_black_user = MagicMock(spec=User)
        mock_session.query.return_value.filter.return_value.first.return_value = mock_game
        mock_session.query.side_effect = [[mock_game], [mock_white_user], [mock_black_user]]

        # Call save_and_update_elo
        self.chess_game.save_and_update_elo()

        # Check that the game and user data was updated correctly
        # self.assertEqual(mock_game.fen, self.chess_game.fen)
        # self.assertEqual(mock_game.moves, ",".join(self.chess_game.moves))
        # self.assertEqual(mock_game.is_finish, self.chess_game._ChessGame__finished)
        # self.assertEqual(mock_game.winner, "white")
        # self.assertEqual(mock_white_user.wins, mock_white_user.wins + 1)
        # self.assertEqual(mock_black_user.losses, mock_black_user.losses + 1)
        # self.assertEqual(mock_white_user.rating, mock_white_user.rating + mock_game.get_point_difference(mock_white_user.user))
        # self.assertEqual(mock_black_user.rating, mock_black_user.rating + mock_game.get_point_difference(mock_black_user.user))

        # Check that the game and users were added to the session
        # mock_session.add_all.assert_called_once_with([mock_black_user, mock_white_user])
        # mock_session.add.assert_called_once_with(mock_game)

        # # Check that the session was committed and closed
        # mock_session.commit.assert_called_once()
        # mock_session.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()