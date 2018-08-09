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
        g.apply_move('e4')
        square_from, square_to = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'Bd3')
        self.assertEqual('f1', square_from.notation())
        self.assertEqual('d3', square_to.notation())

    def test_bishop_capture(self):
        g = castle.Game()
        g.apply_move('e4')
        g.apply_move('e5')
        g.apply_move('d4')
        g.apply_move('a6')
        g.apply_move('Bxa6')
        bishop_square = g.board.square_from_notation('a6')
        self.assertTrue(bishop_square.occupant.type == PieceType.BISHOP)
        self.assertTrue(bishop_square.occupant.color == Color.WHITE)
