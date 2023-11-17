
import unittest
import requests
from backend.config import Config

import asyncio
import websockets

def _auth(jwt:str) -> requests:
    return {'Authorization':  f'{jwt}'}

def default_game_body()-> dict:
    return {
    "against_bot": True,
    "type": "dark_chess"
    }

async def on_open(event):
    print('WebSocket connection opened:', event)

async def on_message(event):
    print('Message from server:', event.data)

async def on_error(event):
    print('WebSocket error:', event)

async def on_close(event):
    print('WebSocket connection closed:', event)


class TestApiGame(unittest.TestCase):

    def setUp(self):
        config = Config()
        self.host =f"{config['host']}:{config['port']}"
        self.base_url = f'http://{self.host}'
        self.base_url_api = f'{self.base_url}/api/v1'
    

    def _create_guest_user(self)->str:
        jwt=requests.post(self.base_url_api + '/user/guest').json()
        return jwt

    def test_join_game(self):
        jwt1 = self._create_guest_user()
        jwt2 = self._create_guest_user()

        game_id = requests.post(self.base_url_api + "/game",headers=_auth(jwt1),json=default_game_body()).json()
        requests.put(self.base_url_api + f"/game/{game_id}/join",headers=_auth(jwt1)).json()
        requests.put(self.base_url_api + f"/game/{game_id}/join",headers=_auth(jwt2)).json()
        print(game_id, flush=True)

        async def socket_conn(auth_token):
            server_url = f"ws://{self.host}/api/v1/game/{game_id}/ws"

            headers = [('Authorization', auth_token)]

            async with websockets.connect(server_url, extra_headers=headers) as websocket:
                await on_open(websocket)
                async for message in websocket:
                    await on_message(message)

                await on_close(websocket)

        async def double_run():
            await asyncio.gather(socket_conn(jwt1), socket_conn(jwt2))

        asyncio.get_event_loop().run_until_complete(double_run())
