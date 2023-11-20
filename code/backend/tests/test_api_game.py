
import json
import unittest
import requests
from backend.config import Config
import json
import asyncio
import time
from websockets.sync.client import connect

def _auth(jwt:str) -> requests:
    return {'Authorization':  f'{jwt}'}

def default_game_body(bot=False)-> dict:
    return {
        "against_bot": bot,
        "type": "dark_chess"
    }


def _go_listening_until_move(ws, name=None):
    while True:
        message = ws.recv()
        if "waiting" not in json.loads(message):
            return message


class TestApiGame(unittest.TestCase):

    def setUp(self):
        config = Config()
        self.host =f"{config['host']}:{config['port']}"
        self.base_url = f'http://{self.host}'
        self.base_url_api = f'{self.base_url}/api/v1'
    

    def _create_guest_user(self)->str:
        jwt=requests.post(self.base_url_api + '/user/guest').json()
        return jwt

    def test_join_game_bot_black(self):
        jwt = self._create_guest_user()

        game_id = requests.post(self.base_url_api + "/game",headers=_auth(jwt),json=default_game_body(True)).json()
        requests.put(self.base_url_api + f"/game/{game_id}/join/black",headers=_auth(jwt)).json()

        server_url = lambda x: f"ws://{self.host}/api/v1/game/{game_id}/{x}/ws"

        def player(auth_token):
            with connect(server_url(auth_token)) as websocket:
                message = websocket.recv()
                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a7a6"}))
                message = websocket.recv()
                _go_listening_until_move(websocket,'black player ')
                websocket.send(json.dumps({"kind": "move", "data": "a6a5"}))
                message = websocket.recv()

            websocket.close()


        import threading
        t = threading.Thread(target=player, args=(jwt,))
        t.start()
        t.join()


    def test_join_game_bot(self):
        jwt = self._create_guest_user()

        game_id = requests.post(self.base_url_api + "/game",headers=_auth(jwt),json=default_game_body(True)).json()
        requests.put(self.base_url_api + f"/game/{game_id}/join",headers=_auth(jwt)).json()

        server_url = lambda x: f"ws://{self.host}/api/v1/game/{game_id}/{x}/ws"

        def player(auth_token):
            with connect(server_url(auth_token)) as websocket:
                message = websocket.recv()
                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))
                message = websocket.recv()
                _go_listening_until_move(websocket,'first player ')
                websocket.send(json.dumps({"kind": "move", "data": "a3a4"}))
                message = websocket.recv()

            websocket.close()


        import threading
        t = threading.Thread(target=player, args=(jwt,))
        t.start()
        t.join()

    def test_join_game(self):
        jwt1 = self._create_guest_user()
        jwt2 = self._create_guest_user()

        game_id = requests.post(self.base_url_api + "/game",headers=_auth(jwt1),json=default_game_body()).json()
        requests.put(self.base_url_api + f"/game/{game_id}/join",headers=_auth(jwt1)).json()
        requests.put(self.base_url_api + f"/game/{game_id}/join",headers=_auth(jwt2)).json()

        server_url = lambda x: f"ws://{self.host}/api/v1/game/{game_id}/{x}/ws"

        def first_player(auth_token):

            with connect(server_url(auth_token)) as websocket:
                message = websocket.recv()
                time.sleep(2)
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))
                message = websocket.recv()
                _go_listening_until_move(websocket,'first player ')

            websocket.close()

        def second_player(auth_token):
            with connect(server_url(auth_token)) as websocket:
                message = websocket.recv() 
                _go_listening_until_move(websocket,'second player ')
                 
                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))
                message = websocket.recv()

                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a7a6"}))
                message = websocket.recv()                

            websocket.close()

        # open two thread 
        # one for each player
        import threading
        t1 = threading.Thread(target=first_player, args=(jwt1,))
        t2 = threading.Thread(target=second_player, args=(jwt2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        



