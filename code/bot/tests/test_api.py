import unittest
from unittest.mock import patch, MagicMock
from bot.api_utils import create_game, delete_game, get_user, make_move
from bot.config import backend_url, api_base_url
from bot.ws_utils import GameStatus, WaitingStatus, WebSocketWrapper


test_token = "test_token"
test_game_id = 10
test_move = "e2e4"
test_game_status = GameStatus(
    {
        "move_made": None,
        "ended": False,
        "view": "rbkqbbnr/pppppppp/8/8/8/8/PPPPPPPP/RBKQBBNR",
        "possible_moves": ["e2e4", "e2e3", "g1f3", "b1c3"],
        "turn": "white",
    }
)

test_waiting_status = WaitingStatus({"waiting": True})


class TestGameApi(unittest.TestCase):
    @patch("bot.api_utils.requests.post")
    @patch("bot.api_utils.requests.put")
    @patch("bot.api_utils.GameMapper")
    @patch("bot.api_utils.get_user")
    def test_create_game(self, mock_get_user, mock_game_mapper, mock_put, mock_post):
        # Set up the mock objects
        mock_get_user.return_value = test_token
        mock_game_mapper_instance = MagicMock()
        mock_game_mapper.return_value = mock_game_mapper_instance
        mock_game_mapper_instance.get.return_value = None
        mock_post.return_value.json.return_value = test_game_id

        # Call the function with a test chat_id and color
        result = create_game(123, "black")

        # Check that the mocks were called with the correct arguments
        mock_get_user.assert_called_once_with(123)
        mock_game_mapper_instance.get.assert_called_once_with(123)
        mock_post.assert_called_once_with(
            f"{backend_url}{api_base_url}/game",
            json={"against_bot": True, "type": "dark_chess", "time": 0},
            headers={"Authorization": test_token},
        )
        mock_put.assert_called_once_with(
            f"{backend_url}{api_base_url}/game/{test_game_id}/join/black",
            headers={"Authorization": test_token},
        )
        mock_game_mapper_instance.add.assert_called_once_with(123, test_game_id)

        # Check that the function returned the correct result
        self.assertEqual(result, (test_token, test_game_id))

    @patch("bot.api_utils.requests.post")
    @patch("bot.api_utils.requests.put")
    @patch("bot.api_utils.GameMapper")
    @patch("bot.api_utils.get_user")
    def test_create_game_already_exists(
        self, mock_get_user, mock_game_mapper, mock_put, mock_post
    ):
        # Set up the mock objects
        mock_get_user.return_value = test_token
        mock_game_mapper_instance = MagicMock()
        mock_game_mapper.return_value = mock_game_mapper_instance
        mock_game_mapper_instance.get.return_value = test_game_id

        # Call the function with a test chat_id and color
        result = create_game(123, "black")

        # Check that the mocks were called with the correct arguments
        mock_get_user.assert_called_once_with(123)
        mock_game_mapper_instance.get.assert_called_once_with(123)
        mock_post.assert_not_called()
        mock_put.assert_not_called()
        mock_game_mapper_instance.add.assert_not_called()

        # Check that the function returned the correct result
        self.assertEqual(result, (test_token, test_game_id))

    @patch("bot.api_utils.requests.post")
    @patch("bot.api_utils.requests.put")
    @patch("bot.api_utils.GameMapper")
    @patch("bot.api_utils.get_user")
    def test_create_game_with_exception(
        self, mock_get_user, mock_game_mapper, mock_put, mock_post
    ):
        # Set up the mock objects
        mock_get_user.return_value = test_token
        mock_game_mapper_instance = MagicMock()
        mock_game_mapper.return_value = mock_game_mapper_instance
        mock_game_mapper_instance.get.return_value = None
        mock_post.return_value.json.side_effect = Exception("test_exception")

        # Call the function with a test chat_id and color
        with self.assertRaises(Exception):
            create_game(123, "black")

        # Check that the mocks were called with the correct arguments
        mock_get_user.assert_called_once_with(123)
        mock_game_mapper_instance.get.assert_called_once_with(123)
        mock_post.assert_called_once_with(
            f"{backend_url}{api_base_url}/game",
            json={"against_bot": True, "type": "dark_chess", "time": 0},
            headers={"Authorization": test_token},
        )
        mock_put.assert_not_called()
        mock_game_mapper_instance.add.assert_not_called()

    @patch("bot.api_utils.requests.post")
    @patch("bot.api_utils.UserMapper")
    def test_get_user(self, mock_user_mapper, mock_post):
        # Set up the mock objects
        mock_user_mapper_instance = MagicMock()
        mock_user_mapper.return_value = mock_user_mapper_instance
        mock_user_mapper_instance.get.return_value = None
        mock_post.return_value.json.return_value = test_token

        # Call the function with a test chat_id
        result = get_user(123)

        # Check that the mocks were called with the correct arguments
        mock_user_mapper_instance.get.assert_called_once_with(123)
        mock_post.assert_called_once_with(f"{backend_url}{api_base_url}/user/guest")
        mock_user_mapper_instance.add.assert_called_once_with(123, test_token)

        # Check that the function returned the correct result
        self.assertEqual(result, test_token)

    @patch("bot.api_utils.requests.post")
    @patch("bot.api_utils.UserMapper")
    def test_get_user_already_exists(self, mock_user_mapper, mock_posts):
        # Set up the mock objects
        mock_user_mapper_instance = MagicMock()
        mock_user_mapper.return_value = mock_user_mapper_instance
        mock_user_mapper_instance.get.return_value = test_token
        mock_posts.return_value.json.return_value = test_token

        # Call the function with a test chat_id
        result = get_user(123)

        # Check that the mocks were called with the correct arguments
        mock_user_mapper_instance.get.assert_called_once_with(123)
        mock_user_mapper_instance.add.assert_not_called()
        mock_posts.assert_not_called()

        # Check that the function returned the correct result
        self.assertEqual(result, test_token)

    @patch("bot.api_utils.requests.post")
    @patch("bot.api_utils.UserMapper")
    def test_get_user_with_exception(self, mock_user_mapper, mock_post):
        # Set up the mock objects
        mock_user_mapper_instance = MagicMock()
        mock_user_mapper.return_value = mock_user_mapper_instance
        mock_user_mapper_instance.get.return_value = None
        mock_post.return_value.json.side_effect = Exception("test_exception")

        # Call the function with a test chat_id
        with self.assertRaises(Exception):
            create_game(123)

        # Check that the mocks were called with the correct arguments
        mock_user_mapper_instance.get.assert_called_once_with(123)
        mock_post.assert_called_once_with(f"{backend_url}{api_base_url}/user/guest")
        mock_user_mapper_instance.add.assert_not_called()

    @patch("bot.api_utils.GameMapper")
    def test_delete_game(self, mock_game_mapper):
        # Set up the mock objects
        mock_game_mapper_instance = MagicMock()
        mock_game_mapper.return_value = mock_game_mapper_instance
        mock_game_mapper_instance.get.return_value = test_game_id

        # Call the function with a test chat_id
        delete_game(123)

        # Check that the mocks were called with the correct arguments
        mock_game_mapper_instance.get.assert_called_once_with(123)
        mock_game_mapper_instance.remove.assert_called_once_with(123)

    @patch("bot.api_utils.GameMapper")
    def test_delete_game_not_exists(self, mock_game_mapper):
        # Set up the mock objects
        mock_game_mapper_instance = MagicMock()
        mock_game_mapper.return_value = mock_game_mapper_instance
        mock_game_mapper_instance.get.return_value = None

        # Call the function with a test chat_id
        delete_game(123)

        # Check that the mocks were called with the correct arguments
        mock_game_mapper_instance.get.assert_called_once_with(123)
        mock_game_mapper_instance.remove.assert_not_called()


@unittest.skip("Not implemented")
class TestWsApi(unittest.IsolatedAsyncioTestCase):
    @patch("bot.api_utils.WebSocketWrapper")
    async def test_make_move(self, mock_websocket_wrapper):
        # Set up the mock objects
        mock_websocket_instance = MagicMock()
        mock_websocket_wrapper.return_value = mock_websocket_instance
        mock_websocket_instance.recv.return_value = test_game_status

        # Call the function with a test WebSocketWrapper and move
        result = await make_move(mock_websocket_instance, test_move)

        # Check that the mocks were called with the correct arguments
        mock_websocket_instance.send.assert_called_once_with(
            {"kind": "move", "data": test_move}
        )
        mock_websocket_instance.recv.assert_awaited_once()

        # Check that the function returned the correct result
        self.assertEqual(result, test_game_status)

    @patch("bot.api_utils.WebSocketWrapper")
    async def test_make_move_with_waiting_status(self, mock_websocket_wrapper):
        # Set up the mock objects
        mock_websocket_instance = MagicMock()
        mock_websocket_wrapper.return_value = mock_websocket_instance
        mock_websocket_instance.recv.return_value = test_waiting_status

        # Call the function with a test WebSocketWrapper and move
        with self.assertRaises(ValueError):
            await make_move(mock_websocket_instance, test_move)

        # Check that the mocks were called with the correct arguments
        mock_websocket_instance.send.assert_called_once_with(
            {"kind": "move", "data": test_move}
        )
        mock_websocket_instance.recv.assert_awaited_once()
