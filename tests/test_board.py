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

    def test_get_rook_moves(self):
        board = Board()
        board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'e5')
        board.place_piece(Piece(PieceType.ROOK, Color.WHITE), 'c5')
        board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'c3')
        board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'e6')
        self.assertEqual(
            board.get_moves(board.square_from_notation('c5')),
            {
                board.square_from_notation('a5'),
                board.square_from_notation('b5'),
                board.square_from_notation('d5'),
                board.square_from_notation('c4'),
                board.square_from_notation('c6'),
                board.square_from_notation('c7'),
                board.square_from_notation('c8'),
                board.square_from_notation('c3')
            }
        )
        self.assertEqual(
            board.get_moves(board.square_from_notation('e6')),
            {
                board.square_from_notation('a6'),
                board.square_from_notation('b6'),
                board.square_from_notation('c6'),
                board.square_from_notation('d6'),
                board.square_from_notation('f6'),
                board.square_from_notation('g6'),
                board.square_from_notation('h6'),
                board.square_from_notation('e5'),
                board.square_from_notation('e7'),
                board.square_from_notation('e8')
            }
        )

    def test_bishop_moves(self):
        board = Board()
        board.place_piece(Piece(PieceType.BISHOP, Color.WHITE), 'c4')
        board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'e6')
        board.place_piece(Piece(PieceType.BISHOP, Color.WHITE), 'd3')
        board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'd7')
        self.assertEqual(
            board.get_moves(board.square_from_notation('c4')),
            {
                board.square_from_notation('a2'),
                board.square_from_notation('b3'),
                board.square_from_notation('b5'),
                board.square_from_notation('a6'),
                board.square_from_notation('d5'),
                board.square_from_notation('e6')
            }
        )
        self.assertEqual(
            board.get_moves(board.square_from_notation('e6')),
            {
                board.square_from_notation('d5'),
                board.square_from_notation('c4'),
                board.square_from_notation('f7'),
                board.square_from_notation('g8'),
                board.square_from_notation('f5'),
                board.square_from_notation('g4'),
                board.square_from_notation('h3')
            }
        )

    def test_knight_moves(self):
        board = Board()
        board.place_piece(Piece(PieceType.KNIGHT, Color.WHITE), 'b6')
        board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'e4')
        board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'c3')
        board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'd5')
        board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'f6')
        self.assertEqual(
            board.get_moves(board.square_from_notation('b6')),
            {
                board.square_from_notation('a8'),
                board.square_from_notation('c8'),
                board.square_from_notation('d7'),
                board.square_from_notation('d5'),
                board.square_from_notation('c4'),
                board.square_from_notation('a4'),
            }
        )
        self.assertEqual(
            board.get_moves(board.square_from_notation('e4')),
            {
                board.square_from_notation('d6'),
                board.square_from_notation('g5'),
                board.square_from_notation('g3'),
                board.square_from_notation('f2'),
                board.square_from_notation('d2'),
                board.square_from_notation('c3'),
                board.square_from_notation('c5')
            }
        )

    def test_queen_moves(self):
        board = Board()
        board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'a2')
        board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'c6')
        board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'd2')
        board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'f7')
        board.place_piece(Piece(PieceType.QUEEN, Color.WHITE), 'd5')
        board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'b5')
        board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'f3')
        board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'g5')
        self.assertEqual(
            board.get_moves(board.square_from_notation('d5')),
            {
                board.square_from_notation('c5'),
                board.square_from_notation('b5'),
                board.square_from_notation('c4'),
                board.square_from_notation('b3'),
                board.square_from_notation('d4'),
                board.square_from_notation('d3'),
                board.square_from_notation('e4'),
                board.square_from_notation('f3'),
                board.square_from_notation('e5'),
                board.square_from_notation('f5'),
                board.square_from_notation('g5'),
                board.square_from_notation('e6'),
                board.square_from_notation('d6'),
                board.square_from_notation('d7'),
                board.square_from_notation('d8'),

            }
        )

    def test_pawn_pushed_forward(self):
        board = Board()
        board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'a8')
        board.get_moves(board.square_from_notation('a8'))
