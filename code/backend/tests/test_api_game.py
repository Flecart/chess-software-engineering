import json
import unittest
import requests
import time
from backend.config import Config
from websockets.sync.client import connect


def _auth(jwt: str) -> requests:
    return {"Authorization": f"{jwt}"}


def default_game_body(bot=False) -> dict:
    return {"against_bot": bot, "type": "dark_chess"}


def _go_listening_until_move(ws, name=None):
    while True:
        message = json.loads(ws.recv())
        if "waiting" not in message:
            return message


def _play_moves(websocket, name, moves):
    def checked(message):
        return (
            isinstance(message, dict)
            and "ended" in message
            and message["ended"] is True
        )

    for i, move in enumerate(moves):
        time.sleep(2)
        websocket.send(json.dumps({"kind": "move", "data": move}))
        message = json.loads(websocket.recv())
        if checked(message):
            return i
        message = _go_listening_until_move(websocket, name)
        if checked(message):
            return i

    return None


@unittest.skip("Not useful")
class TestApiGame(unittest.TestCase):
    def setUp(self):
        config = Config()
        self.host = f"{config['host']}:{config['port']}"
        self.base_url = f"http://{self.host}"
        self.base_url_api = f"{self.base_url}/api/v1"
        self.websocket_url = (
            lambda game_id, token: f"ws://{self.host}/api/v1/game/{game_id}/ws?token={token}"
        )

    def _two_player_play(self, white, black, moves_white, moves_black, game_id):
        def first_player(auth_token):
            with connect(self.websocket_url(game_id, auth_token)) as websocket:
                message = json.loads(websocket.recv())
                if message["turn"] == "black":
                    _go_listening_until_move(websocket, "black")
                _play_moves(websocket, "white", moves_white)
                websocket.close()

        def second_player(auth_token):
            with connect(self.websocket_url(game_id, auth_token)) as websocket:
                message = json.loads(websocket.recv())
                if message["turn"] == "white":
                    _go_listening_until_move(websocket, "black")
                _play_moves(websocket, "black", moves_black)
                websocket.close()

        import threading

        t1 = threading.Thread(target=first_player, args=(white,))
        t2 = threading.Thread(target=second_player, args=(black,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def _login(self, user, psw) -> str:
        data = requests.post(
            self.base_url_api + "/user/login", json={"username": user, "password": psw}
        ).json()
        return data

    def _sign_up(self, user, psw) -> str:
        data = requests.post(
            self.base_url_api + "/user/signup", json={"username": user, "password": psw}
        ).json()
        if not isinstance(data, str):
            raise Exception()
        return data

    def _create_guest_user(self) -> str:
        jwt = requests.post(self.base_url_api + "/user/guest").json()
        return jwt

    def test_join_game_bot_black(self):
        jwt = self._create_guest_user()

        game_id = requests.post(
            self.base_url_api + "/game",
            headers=_auth(jwt),
            json=default_game_body(True),
        ).json()
        requests.put(
            self.base_url_api + f"/game/{game_id}/join/black", headers=_auth(jwt)
        ).json()

        def player(auth_token):
            with connect(self.websocket_url(game_id, auth_token)) as websocket:
                websocket.recv()
                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a7a6"}))
                websocket.recv()
                _go_listening_until_move(websocket, "black player ")
                websocket.send(json.dumps({"kind": "move", "data": "a6a5"}))
                websocket.recv()

            websocket.close()

        import threading

        t = threading.Thread(target=player, args=(jwt,))
        t.start()
        t.join()

    def test_join_game_bot_wrong_move(self):
        jwt = self._create_guest_user()

        game_id = requests.post(
            self.base_url_api + "/game",
            headers=_auth(jwt),
            json=default_game_body(True),
        ).json()
        requests.put(
            self.base_url_api + f"/game/{game_id}/join/", headers=_auth(jwt)
        ).json()

        def player(auth_token):
            with connect(self.websocket_url(game_id, auth_token)) as websocket:
                websocket.recv()
                websocket.send(json.dumps({"kind": "move", "data": "a1a3"}))
                websocket.recv()
                websocket.send(json.dumps({"kind": "move", "data": "a3a4"}))
                websocket.recv()

            websocket.close()

        import threading

        t = threading.Thread(target=player, args=(jwt,))
        t.start()
        t.join()

    def test_join_game_bot(self):
        jwt = self._create_guest_user()

        game_id = requests.post(
            self.base_url_api + "/game",
            headers=_auth(jwt),
            json=default_game_body(True),
        ).json()
        requests.put(
            self.base_url_api + f"/game/{game_id}/join/", headers=_auth(jwt)
        ).json()

        def player(auth_token):
            with connect(self.websocket_url(game_id, auth_token)) as websocket:
                websocket.recv()
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))
                websocket.recv()
                _go_listening_until_move(websocket, "first player ")
                websocket.send(json.dumps({"kind": "move", "data": "a3a4"}))
                websocket.recv()

            websocket.close()

        import threading

        t = threading.Thread(target=player, args=(jwt,))
        t.start()
        t.join()

    def test_join_game(self):
        jwt1 = self._create_guest_user()
        jwt2 = self._create_guest_user()

        game_id = requests.post(
            self.base_url_api + "/game", headers=_auth(jwt1), json=default_game_body()
        ).json()
        requests.put(
            self.base_url_api + f"/game/{game_id}/join/", headers=_auth(jwt1)
        ).json()
        requests.put(
            self.base_url_api + f"/game/{game_id}/join/", headers=_auth(jwt2)
        ).json()

        def first_player(auth_token):
            with connect(self.websocket_url(game_id, auth_token)) as websocket:
                websocket.recv()
                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))
                websocket.recv()
                _go_listening_until_move(websocket, "first")
            websocket.close()

        def second_player(auth_token):
            with connect(self.websocket_url(game_id, auth_token)) as websocket:
                websocket.recv()
                _go_listening_until_move(websocket, "second player ")
                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a2a3"}))
                websocket.recv()
                time.sleep(1)
                websocket.send(json.dumps({"kind": "move", "data": "a7a6"}))
                websocket.recv()

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

    def test_leaderboard(self):
        credentials = [
            ["user1", "user"],
            ["user2", "user"],
            ["user3", "user"],
            ["user4", "user"],
        ]
        moves_black = ["f7f5", "a7a6", "d3d3"]
        moves_white = ["e2e4", "d1h5", "h5e8"]
        jwt = []
        for [user, psw] in credentials:
            try:
                jwt.append(self._sign_up(user, psw))
            except Exception:
                jwt.append(self._login(user, psw))

        versus = [(0, 1), (1, 2), (1, 3), (1, 0)]

        for w, b in versus:
            game_id = requests.post(
                self.base_url_api + "/game",
                headers=_auth(jwt[w]),
                json=default_game_body(False),
            ).json()
            requests.put(
                self.base_url_api + f"/game/{game_id}/join/white", headers=_auth(jwt[w])
            ).json()
            requests.put(
                self.base_url_api + f"/game/{game_id}/join/black", headers=_auth(jwt[b])
            ).json()
            self._two_player_play(jwt[w], jwt[b], moves_white, moves_black, game_id)
