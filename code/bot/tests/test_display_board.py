import unittest
from bot.display_board import _to_standard_fen, _get_not_visible_squares

test_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq 0 1"


class TestToStandardFen(unittest.TestCase):
    def test_fen_with_empty_cells(self):
        self.assertEqual(
            _to_standard_fen(test_fen),
            test_fen,
        )

    def test_fen_with_question_marks(self):
        self.assertEqual(
            _to_standard_fen(
                "rnbqkbnr/pppppppp/8/8/4P?2/8/PPPP1PPP/RNBQKBNR b KQkq 0 1"
            ),
            test_fen,
        )

    def test_obscured_black_fen(self):
        self.assertEqual(
            _to_standard_fen(
                "????????/????????/8/8/4P2/8/PPPP1PPP/RNBQKBNR b KQkq 0 1"
            ),
            "8/8/8/8/4P2/8/PPPP1PPP/RNBQKBNR b KQkq 0 1",
        )

    def test_obscured_white_fen(self):
        self.assertEqual(
            _to_standard_fen(
                "rnbqkbnr/pppppppp/8/8/4P2/8/????????/???????? b KQkq 0 1"
            ),
            "rnbqkbnr/pppppppp/8/8/4P2/8/8/8 b KQkq 0 1",
        )


class TestGetNotVisibleSquares(unittest.TestCase):
    def test_fen_with_no_question_marks(self):
        self.assertEqual(
            set(_get_not_visible_squares(test_fen)),
            set(),
        )

    def test_fen_with_one_question_mark(self):
        self.assertEqual(
            set(
                _get_not_visible_squares(
                    "rnbqkbnr/pppppppp/8/8/4P?2/8/PPPP1PPP/RNBQKBNR b KQkq 0 1"
                )
            ),
            set([(3, 6)]),
        )

    def test_fen_with_multiple_question_marks(self):
        self.assertEqual(
            set(
                _get_not_visible_squares(
                    "rnbqkbnr/pppppppp/8/8/4P?2/8/PPPP1?PP/RNBQKBNR b KQkq 0 1"
                )
            ),
            set([(1, 6), (3, 6)]),
        )

    def test_fen_with_all_question_marks(self):
        self.assertEqual(
            set(
                _get_not_visible_squares(
                    "????????/????????/????????/????????/????????/????????/????????/???????? b KQkq 0 1"
                )
            ),
            set(
                [
                    (7, 1),
                    (7, 2),
                    (7, 3),
                    (7, 4),
                    (7, 5),
                    (7, 6),
                    (7, 7),
                    (7, 8),
                    (6, 1),
                    (6, 2),
                    (6, 3),
                    (6, 4),
                    (6, 5),
                    (6, 6),
                    (6, 7),
                    (6, 8),
                    (5, 1),
                    (5, 2),
                    (5, 3),
                    (5, 4),
                    (5, 5),
                    (5, 6),
                    (5, 7),
                    (5, 8),
                    (4, 1),
                    (4, 2),
                    (4, 3),
                    (4, 4),
                    (4, 5),
                    (4, 6),
                    (4, 7),
                    (4, 8),
                    (3, 1),
                    (3, 2),
                    (3, 3),
                    (3, 4),
                    (3, 5),
                    (3, 6),
                    (3, 7),
                    (3, 8),
                    (2, 1),
                    (2, 2),
                    (2, 3),
                    (2, 4),
                    (2, 5),
                    (2, 6),
                    (2, 7),
                    (2, 8),
                    (1, 1),
                    (1, 2),
                    (1, 3),
                    (1, 4),
                    (1, 5),
                    (1, 6),
                    (1, 7),
                    (1, 8),
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 4),
                    (0, 5),
                    (0, 6),
                    (0, 7),
                    (0, 8),
                ]
            ),
        )
