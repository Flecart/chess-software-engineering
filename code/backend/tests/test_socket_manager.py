import unittest

from backend.game.v1_socket_manager import SocketManager
from backend.game.v1_chess_game_manager import ChessGameManager
from backend.game.v1_chess_game import CreateGameRequest, Color


class TestSocketManager(unittest.TestCase):
    def setUp(self):
        self.socket_manager = SocketManager()

    async def test_add_socket(self):
        # create a mock object that exec the function send_json
        game_request = CreateGameRequest(type="dark_chess", against_bot=False, time=10)
        game_id = ChessGameManager().create_new_game(game_request)

        class MockSocket:
            async def send_json(self, data):
                self.data = data

        socket1 = MockSocket()
        socket2 = MockSocket()

        await self.socket_manager.join(game_id, "test", socket1)
        await self.socket_manager.join(game_id, "test", socket2)
        await self.socket_manager.is_socket_reading(game_id, socket1)
        await self.socket_manager.notify_opponent(game_id, socket1, Color.WHITE)
        await self.socket_manager.remove(game_id, "test", socket2)
