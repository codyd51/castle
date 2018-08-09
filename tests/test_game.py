import unittest

import castle
from castle import Game, Board, Piece, PieceType, Color, InvalidChessNotationError


class GameTests(unittest.TestCase):
    def check_contains_piece(self, game: Game, square_notation: str, piece_type: PieceType, piece_color: Color):
        square = game.board.square_from_notation(square_notation)
        self.assertEqual(piece_type, square.occupant.type)
        self.assertEqual(piece_color, square.occupant.color)

    def test_simple(self):
        g = castle.Game()
        square_from, square_to = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'e4')
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
        self.check_contains_piece(g, 'a6', PieceType.BISHOP, Color.WHITE)

    def test_pawn_capture(self):
        g = castle.Game()
        g.apply_move('e4')
        g.apply_move('f5')
        # TODO(PT): once MoveParser returns a Move object, this should verify a capture was indicated
        g.apply_move('exf5')
        self.check_contains_piece(g, 'f5', PieceType.PAWN, Color.WHITE)

    def test_knight_movement(self):
        g = castle.Game()
        g.apply_move('e4')
        g.apply_move('e5')
        g.apply_move('Ne2')
        self.check_contains_piece(g, 'e2', PieceType.KNIGHT, Color.WHITE)

    def test_ambiguous_knight_movement(self):
        g = castle.Game()
        g.apply_move('e4')
        g.apply_move('e5')
        g.apply_move('Ne2')
        g.apply_move('f6')
        with self.assertRaises(InvalidChessNotationError):
            g.apply_move('Nc3')

        g.apply_move('Nec3')
        self.check_contains_piece(g, 'c3', PieceType.KNIGHT, Color.WHITE)
