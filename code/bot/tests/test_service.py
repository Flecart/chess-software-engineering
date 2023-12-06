import unittest
from bot.src.user_mapper import UserMapper
from bot.src.game_mapper import GameMapper
from bot.src.ballot_box_collection import BallotBoxCollection


class TestGameMapper(unittest.TestCase):
    def setUp(self):
        self.game_mapper = GameMapper()

    def test_add(self):
        self.game_mapper.add(1, 100)
        self.assertEqual(self.game_mapper.get(1), 100)

    def test_get(self):
        self.game_mapper.add(2, 200)
        self.assertEqual(self.game_mapper.get(2), 200)
        self.assertIsNone(self.game_mapper.get(3))

    def test_remove(self):
        self.game_mapper.add(3, 300)
        self.assertEqual(self.game_mapper.get(3), 300)
        self.game_mapper.remove(3)
        self.assertIsNone(self.game_mapper.get(3))

    def test_singleton(self):
        mapper1 = GameMapper()
        mapper2 = GameMapper()
        self.assertEqual(id(mapper1), id(mapper2))


class TestUserMapper(unittest.TestCase):
    def setUp(self):
        self.user_mapper = UserMapper()

    def test_add(self):
        self.user_mapper.add(1, "token1")
        self.assertEqual(self.user_mapper.get(1), "token1")

    def test_get(self):
        self.user_mapper.add(2, "token2")
        self.assertEqual(self.user_mapper.get(2), "token2")
        self.assertIsNone(self.user_mapper.get(3))

    def test_remove(self):
        self.user_mapper.add(3, "token3")
        self.assertEqual(self.user_mapper.get(3), "token3")
        self.user_mapper.remove(3)
        self.assertIsNone(self.user_mapper.get(3))

    def test_singleton(self):
        mapper1 = UserMapper()
        mapper2 = UserMapper()
        self.assertEqual(id(mapper1), id(mapper2))


class TestBallotBoxCollection(unittest.TestCase):
    def setUp(self):
        self.ballot_box_collection = BallotBoxCollection()

    def test_add_vote(self):
        self.ballot_box_collection.add_vote(1, 100, "e2e4")
        self.assertEqual(self.ballot_box_collection._vote[1]["e2e4"], [100])

    def test_add_vote_existing_user(self):
        self.ballot_box_collection.add_vote(1, 100, "e2e4")
        self.ballot_box_collection.add_vote(1, 100, "d2d4")
        self.assertEqual(self.ballot_box_collection._vote[1]["e2e4"], [])
        self.assertEqual(self.ballot_box_collection._vote[1]["d2d4"], [100])

    def test_reset_box(self):
        self.ballot_box_collection.add_vote(1, 100, "e2e4")
        self.ballot_box_collection.add_vote(2, 100, "e2e4")
        self.ballot_box_collection.reset_box(1)
        self.assertEqual(self.ballot_box_collection._vote.get(1), None)
        self.assertEqual(self.ballot_box_collection._vote[2]["e2e4"], [100])

    def test_most_voted(self):
        self.ballot_box_collection.reset_box(1)
        self.ballot_box_collection.add_vote(1, 100, "e2e4")
        self.ballot_box_collection.add_vote(1, 101, "e2e4")
        self.ballot_box_collection.add_vote(1, 102, "d2d4")
        self.assertEqual(self.ballot_box_collection.mostVoted(1), ["e2e4"])

    def test_most_voted_tie(self):
        self.ballot_box_collection.reset_box(1)
        self.ballot_box_collection.add_vote(1, 100, "e2e4")
        self.ballot_box_collection.add_vote(1, 101, "d2d4")
        self.assertEqual(self.ballot_box_collection.mostVoted(1), ["e2e4", "d2d4"])

    def test_most_voted_empty(self):
        self.assertEqual(self.ballot_box_collection.mostVoted(3), None)
