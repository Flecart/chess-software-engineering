import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.database import Base, get_db
from backend.routes.auth import create_guest_access_token
from backend.routes.user.data import (
    InfoUser,
    LoginCredentials,
)
from backend.routes.user.user import create_user_routes

engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


def _token():
    import random

    return create_guest_access_token(random.randint(0, 100000))


def _auth():
    return {"Authorization": _token()}


class TestUserRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = FastAPI()
        create_user_routes(cls.app)
        cls.app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(cls.app)

    @patch("backend.routes.user.user.create_guest_access_token")
    def test_guest(self, mock_create_guest_access_token):
        token = _token()
        mock_create_guest_access_token.return_value = token
        response = self.client.post("/user/guest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), token)

    @patch("backend.routes.user.user.check_login")
    @patch("backend.routes.user.user.create_login_access_token")
    def test_login_api(self, mock_create_login_access_token, mock_check_login):
        mock_check_login.return_value = True
        mock_create_login_access_token.return_value = "test_token"
        login_credentials = LoginCredentials(username="test", password="test")
        response = self.client.post("/user/login", json=login_credentials.model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "test_token")

    @patch("backend.routes.user.user.create_user")
    @patch("backend.routes.user.user.create_login_access_token")
    def test_create_user_api(self, mock_create_login_access_token, mock_create_user):
        mock_create_user.return_value = True
        mock_create_login_access_token.return_value = "test_token"
        login_credentials = LoginCredentials(username="test", password="test")
        response = self.client.post("/user/signup", json=login_credentials.model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "test_token")

    @unittest.skip("TODO: fix this test")
    def test_info(self):
        response = self.client.get("/user/info/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            InfoUser(
                username="test", avatar="test_url", elo=1000, losses=5, wins=10
            ).model_dump(),
        )

    def test_get_games(self):
        response = self.client.get("/user/games/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [],
        )

    def test_leaderboard(self):
        response = self.client.get("/user/leaderboard")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [],
        )
