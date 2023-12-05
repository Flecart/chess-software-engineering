import unittest
from unittest.mock import Mock
from bot.utils import pretty_print_time, get_user_and_chat_from_message
from datetime import timedelta


class TestGetUserAndChatFromMessage(unittest.TestCase):
    def setUp(self):
        self.message = Mock()

    def test_get_user_and_chat_from_message(self):
        # Test case 1: Check if the function returns the correct user and chat IDs
        self.message.from_user.id = 123
        self.message.chat.id = 456
        expected_output = (456, 123)
        self.assertEqual(get_user_and_chat_from_message(self.message), expected_output)


class TestUtils(unittest.TestCase):
    def test_pretty_print_time(self):
        # Test case 1: Time with days, hours, minutes, and seconds
        td = timedelta(days=2, hours=3, minutes=45, seconds=30)
        expected_output = "2 giorni 3 ore 45 minuti 30 secondi"
        self.assertEqual(pretty_print_time(td), expected_output)

        # Test case 2: Time with only hours, minutes, and seconds
        td = timedelta(hours=1, minutes=30, seconds=45)
        expected_output = "1 ore 30 minuti 45 secondi"
        self.assertEqual(pretty_print_time(td), expected_output)

        # Test case 3: Time with only minutes and seconds
        td = timedelta(minutes=15, seconds=20)
        expected_output = "15 minuti 20 secondi"
        self.assertEqual(pretty_print_time(td), expected_output)

        # Test case 4: Time with only seconds
        td = timedelta(seconds=10)
        expected_output = "10 secondi"
        self.assertEqual(pretty_print_time(td), expected_output)

        # Test case 5: Time with zero values
        td = timedelta(days=0, hours=0, minutes=0, seconds=0)
        expected_output = "0 secondi"
        self.assertEqual(pretty_print_time(td), expected_output)
