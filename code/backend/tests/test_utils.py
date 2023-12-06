import unittest
from unittest.mock import Mock, patch
from backend.database.models import User
from backend.database.utils import check_user_exists, create_user

from backend.routes.user.data import LoginCredentials


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        self.db = Mock()
        self.login = LoginCredentials(username="testuser", password="testpassword")

    @patch("backend.database.utils.check_user_exists", return_value=False)
    @patch("backend.database.utils.generate_salt", return_value="randomsalt")
    @patch("backend.database.utils.pwd_context")
    def test_create_user_success(
        self, mock_pwd_context, mock_generate_salt, mock_check_user_exists
    ):
        mock_pwd_context.hash.return_value = "hashedpassword"
        result = create_user(self.login, self.db)
        self.assertTrue(result)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()

    @patch("backend.database.utils.check_user_exists", return_value=True)
    def test_create_user_exists(self, mock_check_user_exists):
        result = create_user(self.login, self.db)
        self.assertFalse(result)
        self.db.add.assert_not_called()
        self.db.commit.assert_not_called()

    @patch("backend.database.utils.Session")
    def test_check_user_exists_true(self, mock_session):
        mock_session.query().filter().first.return_value = Mock()
        result = check_user_exists("testuser", mock_session)
        self.assertTrue(result)
