import unittest

from castle import Board, Piece, PieceType, Color, InvalidChessNotationError


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

                self.assertEqual(notation, square.__repr__())
                self.assertEqual(file_idx, square.file)
                self.assertEqual(rank_idx, square.rank)

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

                square = self.board._squares[rank_idx][file_idx]
                self.assertEqual(notation, square.__repr__())
                self.assertEqual(file_idx, square.file)
                self.assertEqual(rank_idx, square.rank)

    def test_place_piece(self):
        location = 'a3'
        self.board.place_piece(Piece(PieceType.ROOK, Color.BLACK), location)
        square = self.board.square_from_notation(location)
        self.assertEqual(location, square.__repr__())
        self.assertIsNotNone(square.occupant)
        self.assertEqual(PieceType.ROOK, square.occupant.type)
        self.assertEqual(5, square.occupant.value)
        self.assertEqual(Color.BLACK, square.occupant.color)

    def test_get_pawn_moves(self):
        white_pawn = Piece(PieceType.PAWN, Color.WHITE)
        black_pawn = Piece(PieceType.PAWN, Color.BLACK)
        board = Board()
        board.place_piece(white_pawn, 'd2')
        board.place_piece(white_pawn, 'e2')
        board.place_piece(black_pawn, 'b5')
        board.place_piece(black_pawn, 'f3')
        board.place_piece(black_pawn, 'd3')
        self.assertEqual(
            board.get_moves(board.square_from_notation('b5')),
            {board.square_from_notation('b4')}
        )
        self.assertEqual(
            board.get_moves(board.square_from_notation('f3')),
            {board.square_from_notation('e2'), board.square_from_notation('f2')}
        )
        self.assertEqual(
            board.get_moves(board.square_from_notation('d3')),
            {board.square_from_notation('e2')}
        )
        self.assertEqual(
            board.get_moves(board.square_from_notation('d2')),
            set()
        )
        self.assertEqual(
            board.get_moves(board.square_from_notation('e2')),
            {board.square_from_notation('e3'), board.square_from_notation('e4'),
             board.square_from_notation('d3'), board.square_from_notation('f3')}
        )