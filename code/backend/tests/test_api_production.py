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
        message = json.loads(ws.recv())
        if "waiting" not in message:
            return message

def _play_moves(websocket,name,moves):
    checked = lambda message:type(message) == dict and 'ended' in message and message['ended'] ==True
    for (i,move) in enumerate(moves):
        time.sleep(0.1)
        websocket.send(json.dumps({"kind": "move", "data":move }))
        message = json.loads(websocket.recv())
        print(name,message)
        if checked(message):
            return i
        message = _go_listening_until_move(websocket,name)
        if checked(message):
            return i
        
    return None

class TestApiGame(unittest.TestCase):
    
    def _two_player_play(self,white,black,moves_white,moves_black,game_id):
        def first_player(auth_token):
            with connect(self.websocket_url(game_id,auth_token)) as websocket:
                message = json.loads(websocket.recv())
                if message['turn'] == 'black':
                    _go_listening_until_move(websocket,'black')
                _play_moves(websocket,'white',moves_white)
                websocket.close()

        def second_player(auth_token):
            with connect(self.websocket_url(game_id,auth_token)) as websocket:
                message = json.loads(websocket.recv())
                if message['turn'] == 'white':
                    _go_listening_until_move(websocket,'black')
                _play_moves(websocket,'black',moves_black)
                websocket.close()
            
        import threading
        t1 = threading.Thread(target=first_player, args=(white,))
        t2 = threading.Thread(target=second_player, args=(black,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    
    def _login(self,user,psw)-> str:
        data = requests.post(self.base_url_api+'/user/login', json={
            'username':user,
            'password':psw
        }).json()
        print(data)
        return data



    def _sing_up(self,user,psw)->str:
        data = requests.post(self.base_url_api+'/user/signup',json={
            'username':user,
            'password':psw
        }).json()
        if type(data) != str:
            raise Exception()
        return data


    def setUp(self):
        config = Config()
        self.host =f"{config['host']}:{config['port']}"
        self.base_url = f'http://{self.host}'
        self.base_url_api = f'{self.base_url}/api/v1'
        self.websocket_url = lambda game_id,x: f"ws://{self.host}/api/v1/game/{game_id}/{x}/ws"
    

    def _create_guest_user(self)->str:
        jwt=requests.post(self.base_url_api + '/user/guest').json()
        return jwt



    def test_leaderboard(self):
        credentials = [['gio','gio'], ['pische','pische'], ['angi','angi'], ['fil','fil'],
                       ['diego','diego'],['alle','alle'],['berny','berny'],
                       ['carlsen','carlsen']]
        moves_black= ['f7f5','a7a6','d3d3']
        moves_white= ['e2e4','d1h5','h5e8']
        jwt = [ ]
        for [user,psw] in credentials:
            try:
                jwt.append(self._sing_up(user,psw))
            except:
                jwt.append(self._login(user,psw))
        
        versus = [
            (0,7)
            (0,2)
            (0,3)
            (0,4)
            (0,5)
            (0,5)
            (2,1)
            (6,3)
            (5,4)
            (6,2)
            (5,3)
        ]

        for (w,b) in versus:
            game_id = requests.post(self.base_url_api + "/game",headers=_auth(jwt[w]),json=default_game_body(False)).json()
            print('created ',game_id)
            requests.put(self.base_url_api + f"/game/{game_id}/join/white",headers=_auth(jwt[w])).json()
            requests.put(self.base_url_api + f"/game/{game_id}/join/black",headers=_auth(jwt[b])).json()
            self._two_player_play(jwt[w],jwt[b],moves_white,moves_black,game_id)
        