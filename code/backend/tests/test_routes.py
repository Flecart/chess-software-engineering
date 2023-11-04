import unittest
import uuid
import requests
import re

from backend.config import Config

class TestTest(unittest.TestCase):

   def setUp(self):
      config = Config()
      self.base_url = f'http://{config["host"]}:{config["port"]}'

   def test_test_route(self):
      res = requests.get(self.base_url + '/test')
      self.assertEqual(res.status_code,200)
      self.assertEqual(res.json(),{"Hello": "test"})

class TestGame(unittest.TestCase):

   def setUp(self):
      config = Config()
      self.base_url = f'http://{config["host"]}:{config["port"]}/game'

   def test_game_base_root(self): # ci andra qualcosa qui?
      res = requests.get(self.base_url)
      self.assertEqual(res.status_code, 404)

   def test_create_game(self):
      # Make an HTTP GET request to your API endpoint
      response = requests.get(self.base_url + '/start')

      # Check the response status code
      self.assertEqual(response.status_code, 200)

      # Parse the JSON response
      response_json = response.json()

      # Check if 'game-id' is in the JSON response
      self.assertIn('game-id', response_json)

      # Extract the value of 'game-id'
      session_id = response_json['game-id']

      # Define a regular expression pattern for UUID format (you can customize it)
      uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'

      # Use re.match to check if the 'game-id' value matches the UUID pattern
      self.assertIsNotNone(re.match(uuid_pattern, session_id))


   def test_game_move(self):
      res = requests.get(self.base_url + '/start')
      self.game_id = res.json()['game_id']

      with self.subTest(msg='test UUID malformato'):
         bad_id = 'aa-bb-0042'
         res_bad_id = requests.get(f'{self.base_url}/{bad_id}/move/e4f1')
         self.assertEqual(res_bad_id.status_code,422)

      with self.subTest(msg='test gameID inesistente'):
         inexitent_id = '21ec318f-b3a7-4d82-bb1e-cd479422baf1' # ...well highly improbable
         res_nex_id = requests.get(f'{self.base_url}/{inexitent_id}/move/e4f1')
         self.assertEqual(res_nex_id.status_code, 404)
         self.assertEqual(res_nex_id.json(), {"error": "Game not found"})

      with self.subTest(msg='test meaningless move'):
         bad_move_format = 'z3kg'
         res_bad_move_format = requests.get(f'{self.base_url}/{self.game_id}/move/{bad_move_format}')
         self.assertEqual(res_bad_move_format.status_code,400)
         self.assertEqual(res_bad_move_format.json(),{"error":"Invalid move format"})

      with self.subTest(msg='test invalid move'):
         bad_move = 'a2a1'
         res_bad_move = requests.get(f'{self.base_url}/{self.game_id}/move/{bad_move}')
         self.assertEqual(res_bad_move.status_code,400)
         self.assertEqual(res_bad_move.json(),{"error":"Invalid move"})

      with self.subTest(msg='test good move'):
         good_move = 'a2a3'
         res_good_move = requests.get(f'{self.base_url}/{self.game_id}/move/{good_move}')
         self.assertEqual(res_good_move.status_code,200)

         good_json = res_good_move.json()
         self.assertIn('game_ended',good_json)
         self.assertIn('board',good_json)

         board = good_json['board']

         board_pattern = r'([RNBQKPprnbqk\.X]+\\n){7}([RNBQKPprnbqk\.X]+)'
         
         self.assertIsNone(re.match(board,board_pattern))


      

