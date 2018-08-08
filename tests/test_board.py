import unittest

from castle import Board, InvalidChessNotationError


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_square_from_notation_good(self):
        # try every valid square on the board
        for file_idx in range(8):
            file = chr(ord('a') + file_idx)
            for rank_idx in range(8):
                rank = rank_idx + 1

                notation = f'{file}{rank}'
                square = self.board.square_from_notation(notation)

                self.assertEqual(file_idx, square.file)
                self.assertEqual(rank_idx, square.rank)
                self.assertEqual(square.__repr__(), notation)

    def test_square_from_notation_bad(self):
        # try some invalid notations, and make sure they raise errors
        with self.assertRaises(InvalidChessNotationError):
            self.board.square_from_notation('a0')
        with self.assertRaises(InvalidChessNotationError):
            self.board.square_from_notation('00')
        with self.assertRaises(InvalidChessNotationError):
            self.board.square_from_notation('aa')
        with self.assertRaises(InvalidChessNotationError):
            self.board.square_from_notation('===')

    def test_board_construction(self):
        for rank_idx in range(8):
            rank = rank_idx + 1
            for file_idx in range(8):
                file = chr(ord('a') + file_idx)
                notation = f'{file}{rank}'

                square = self.board.squares[rank_idx][file_idx]
                self.assertEqual(notation, square.__repr__())
                self.assertEqual(file_idx, square.file)
                self.assertEqual(rank_idx, square.rank)
