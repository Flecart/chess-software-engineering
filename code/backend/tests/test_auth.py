import unittest
from unittest.mock import patch
from backend.routes.auth import decode_access_token, JSONException
from jose import jwt


class TestDecodeAccessToken(unittest.TestCase):
    @patch("backend.routes.auth.SECRET_KEY", "mysecret")
    @patch("backend.routes.auth.ALGORITHM", "HS256")
    def test_decode_valid_token(self):
        token = jwt.encode(
            {"guest": "guest1", "sub": "user1"}, "mysecret", algorithm="HS256"
        )
        result = decode_access_token(token)
        self.assertEqual(result, {"username": "user1", "guest": "guest1"})

    @patch("backend.routes.auth.SECRET_KEY", "mysecret")
    @patch("backend.routes.auth.ALGORITHM", "HS256")
    def test_decode_invalid_token(self):
        token = jwt.encode(
            {"guest": "guest1", "sub": "user1"}, "wrongsecret", algorithm="HS256"
        )
        with self.assertRaises(JSONException) as context:
            decode_access_token(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.error, {"message": "Could not validate jwt"})

    @patch("backend.routes.auth.SECRET_KEY", "mysecret")
    @patch("backend.routes.auth.ALGORITHM", "HS256")
    def test_decode_token_without_required_fields(self):
        token = jwt.encode({"guest": "guest1"}, "mysecret", algorithm="HS256")
        with self.assertRaises(JSONException) as context:
            decode_access_token(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.error, {"message": "Could not validate jwt"})
