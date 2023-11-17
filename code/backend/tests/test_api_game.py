
import json
import unittest
import requests
from backend.config import Config
import json
import asyncio
from websockets.sync.client import connect

def _auth(jwt:str) -> requests:
    return {'Authorization':  f'{jwt}'}

def default_game_body()-> dict:
    return {
    "against_bot": True,
    "type": "dark_chess"
    }

def on_open(event):
    print('WebSocket connection opened:', event)

def on_message(event):
    print('Message from server:', event)

def on_error(event):
    print('WebSocket error:', event)

def on_close(event):
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

        server_url = f"ws://{self.host}/api/v1/game/{game_id}/ws"

        def first_player(auth_token):
            headers = [('Authorization', auth_token)]

            with connect(server_url, additional_headers=headers) as websocket:
                on_open(websocket)
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))
                message = websocket.recv()
                    
                on_close(websocket)

        def second_player(auth_token):
            headers = [('Authorization', auth_token)]

            with connect(server_url, additional_headers=headers) as websocket:
                on_open(websocket)
                message = websocket.recv() 
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))

                websocket.send(json.dumps({"kind": "move", "data": "a7a6"}))

                on_close(websocket)
        # open two thread 
        # one for each player
        import threading
        t1 = threading.Thread(target=first_player, args=(jwt1,))
        t2 = threading.Thread(target=second_player, args=(jwt2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        



