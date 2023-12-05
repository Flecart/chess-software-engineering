import unittest
from unittest.mock import patch
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
        self.loop = asyncio.get_event_loop()
        self.ws_wrapper = WebSocketWrapper(test_game_id, test_token)

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
        self.assertTrue(
            "ended" in result
            and "view" in result
            and "possible_moves" in result
            and "turn" in result
            and "move_made" in result
            and "waiting" not in result
        )

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

    @patch("websocket.WebSocket")
    def test_send(self, mock_websocket):
        self.ws_wrapper.ws = mock_websocket
        msg = Message({"kind": "move", "data": "e2e4"})
        self.ws_wrapper.send(msg)
        mock_websocket.send.assert_called_once_with(json.dumps(msg))

    @unittest.expectedFailure
    @patch("websocket.WebSocket")
    def test_recv(self, mock_websocket):
        mock_websocket.return_value.recv.return_value = json.dumps(test_initial_status)
        self.ws_wrapper.ws = mock_websocket
        result = self.loop.run_until_complete(self.ws_wrapper.recv())
        self.assertIsInstance(result, GameStatus)
