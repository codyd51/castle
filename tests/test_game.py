import unittest

import castle
from castle import Board, Piece, PieceType, Color, InvalidChessNotationError


class GameTests(unittest.TestCase):
    def test_simple(self):
        g = castle.Game()
        square_from, square_to = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'e4')
        self.assertEqual('e2', square_from.notation())
        self.assertEqual('e4', square_to.notation())

        square_from, square_to = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'dxe4')
        self.assertEqual('e2', square_from.notation())
        self.assertEqual('e4', square_to.notation())

        # 1. e4 e5 2. Bd3
        g.board.move_piece_to_square(g.board.square_from_notation('e2'), g.board.square_from_notation('e4'))
        square_from, square_to = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'Bd3')
        self.assertEqual('f1', square_from.notation())
        self.assertEqual('d3', square_to.notation())
