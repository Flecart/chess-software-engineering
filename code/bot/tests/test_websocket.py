import unittest
from unittest.mock import patch, MagicMock
import json
import asyncio
from bot.ws_utils import WebSocketWrapper, GameStatus, Message
from bot.config import ws_url, api_base_url

test_game_id = 1
test_token = "token"
test_initial_status = GameStatus(
    ended=False,
    possible_moves=["e2e4", "d2d4"],
    view="????????/????????/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq 0 0",
    move_made=None,
    turn="white",
)
# TODO: fix some of these tests


class TestWebSocketWrapper(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.ws_wrapper = WebSocketWrapper(test_game_id, test_token)

    def tearDown(self):
        self.loop.close()

    def test_init(self):
        self.assertEqual(self.ws_wrapper.game_id, test_game_id)
        self.assertEqual(self.ws_wrapper.token, test_token)
        self.assertIsNone(self.ws_wrapper.ws)
        self.assertIn("1", self.ws_wrapper.url)
        self.assertIn("token", self.ws_wrapper.url)

    @patch("websocket.WebSocket")
    def test_connect(self, mock_websocket):
        mock_websocket.return_value.recv.return_value = json.dumps(test_initial_status)
        result = self.loop.run_until_complete(self.ws_wrapper.connect())
        self.assertIsInstance(result, dict)
        self.assertTrue(is_game_status(result))

    @patch("websocket.WebSocket")
    def test_connect_waiting(self, mock_websocket):
        mock_websocket.return_value.recv.return_value = json.dumps({"waiting": True})
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(self.ws_wrapper.connect())

    def test_get_ws_url(self):
        self.assertEqual(
            self.ws_wrapper.get_ws_url(),
            f"{ws_url}{api_base_url}/game/{test_game_id}/ws?token={test_token}",
        )

    @patch("websocket.WebSocket")
    def test_close(self, mock_websocket):
        self.ws_wrapper.ws = mock_websocket
        self.ws_wrapper.close()
        mock_websocket.close.assert_called_once()

    def test_close_none(self):
        with self.assertRaises(TypeError):
            self.ws_wrapper.close()

    @patch("websocket.WebSocket")
    def test_send(self, mock_websocket):
        self.ws_wrapper.ws = mock_websocket
        msg = Message({"kind": "move", "data": "e2e4"})
        self.ws_wrapper.send(msg)
        mock_websocket.send.assert_called_once_with(json.dumps(msg))

    def test_send_none(self):
        with self.assertRaises(TypeError):
            self.ws_wrapper.send(Message({"kind": "move", "data": "e2e4"}))

    @patch.object(asyncio.AbstractEventLoop, "run_in_executor")
    def test_recv(self, mock_run_in_executor):
        mock_websocket = MagicMock()
        mock_websocket.recv.return_value = json.dumps(test_initial_status)
        mock_run_in_executor.return_value = mock_websocket.recv.return_value
        self.ws_wrapper.ws = mock_websocket

        result = self.loop.run_until_complete(self.ws_wrapper.recv())

        self.assertIsInstance(result, dict)
        self.assertTrue(is_waiting_status(result) or is_game_status(result))

    def test_recv_none(self):
        with self.assertRaises(TypeError):
            self.loop.run_until_complete(self.ws_wrapper.recv())


def is_waiting_status(data):
    return "waiting" in data and isinstance(data["waiting"], bool)


def is_game_status(data):
    return (
        "ended" in data
        and "view" in data
        and "possible_moves" in data
        and "turn" in data
        and "move_made" in data
        and isinstance(data["ended"], bool)
        and isinstance(data["view"], str)
        and (isinstance(data["possible_moves"], list) or data["possible_moves"] is None)
        and isinstance(data["turn"], str)
        and (isinstance(data["move_made"], str) or data["move_made"] is None)
    )
