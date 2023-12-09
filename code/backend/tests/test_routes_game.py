import unittest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.routes.game.game import create_game_routes
from backend.routes.game.data import CreateGameRequest
from backend.game.v1_chess_game_manager import ChessGameManager
from backend.routes.auth import create_guest_access_token

def _token():
    import random
    return create_guest_access_token(random.randint(0, 100000))

def _auth():
    return {"Authorization": _token()}

class TestGameRoutes(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.app = FastAPI()
        create_game_routes(self.app)
        self.client = TestClient(self.app)
        self.game_request = CreateGameRequest()
        self.user_data = {"username": "testuser"}

    @patch.object(ChessGameManager, 'create_new_game')
    def test_create_game(self, mock_create_new_game):
        mock_create_new_game.return_value = 1
        response = self.client.post("/game", json=self.game_request.model_dump(), headers=_auth())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 1)

    @patch.object(ChessGameManager, 'get_game')
    def test_join_game(self, mock_get_game):
        mock_get_game.return_value.join.return_value = True
        response = self.client.put("/game/1/join", json=self.user_data, headers=_auth())
        self.assertEqual(response.status_code, 200)

    @patch.object(ChessGameManager, 'get_game')
    def test_join_game_with_color(self, mock_get_game):
        mock_get_game.return_value.join.return_value = True
        response = self.client.put("/game/1/join/black", json=self.user_data, headers=_auth())
        self.assertEqual(response.status_code, 200)

    # @patch.object(ChessGameManager, 'get_game')
    # @patch.object(SocketManager, 'join')
    # @patch.object(SocketManager, 'is_socket_reading')
    # @patch.object(SocketManager, 'notify_opponent')
    # @patch.object(SocketManager, 'remove')
    # def test_web_socket(self, mock_remove, mock_notify_opponent, mock_is_socket_reading, mock_join, mock_get_game):
      
    #     # Mock the game
    #     mock_game = AsyncMock()
    #     mock_get_game.return_value = mock_game

    #     # Use Starlette's TestClient to create a WebSocket connection
    #     with TestClient(self.app).websocket_connect(f"/game/1/ws?token={_token()}") as websocket:
    #         # Run the websocket function
    #         response = websocket.receive_text()

    #         print(response)
    #         # Check that the functions were called with the correct arguments
    #         mock_get_game.assert_called_once_with(1)
    #         mock_join.assert_called_once_with(1, self.user_data["username"], websocket)
    #         mock_is_socket_reading.assert_called()
    #         mock_notify_opponent.assert_called()
    #         mock_remove.assert_called_once_with(1, self.user_data["username"], websocket)


if __name__ == '__main__':
    unittest.main()