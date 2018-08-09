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
        move = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'e4')
        self.assertEqual('e2', move.from_square.notation())
        self.assertEqual('e4', move.to_square.notation())

        # 1. e4 e5 2. Bd3
        g.apply_notation('e4')
        move = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'Bd3')
        self.assertEqual('f1', move.from_square.notation())
        self.assertEqual('d3', move.to_square.notation())

    def test_bishop_capture(self):
        g = castle.Game()
        g.apply_notation('e4')
        g.apply_notation('e5')
        g.apply_notation('d4')
        g.apply_notation('a6')
        g.apply_notation('Bxa6')
        self.check_contains_piece(g, 'a6', PieceType.BISHOP, Color.WHITE)

    def test_pawn_capture(self):
        g = castle.Game()
        g.apply_notation('e4')
        g.apply_notation('f5')
        # TODO(PT): once MoveParser returns a Move object, this should verify a capture was indicated
        g.apply_notation('exf5')
        self.check_contains_piece(g, 'f5', PieceType.PAWN, Color.WHITE)

    def test_knight_movement(self):
        g = castle.Game()
        g.apply_notation('e4')
        g.apply_notation('e5')
        g.apply_notation('Ne2')
        self.check_contains_piece(g, 'e2', PieceType.KNIGHT, Color.WHITE)

    def test_ambiguous_knight_movement(self):
        g = castle.Game()
        g.apply_notation('e4')
        g.apply_notation('e5')
        g.apply_notation('Ne2')
        g.apply_notation('f6')
        with self.assertRaises(InvalidChessNotationError):
            g.apply_notation('Nc3')

        g.apply_notation('Nec3')
        self.check_contains_piece(g, 'c3', PieceType.KNIGHT, Color.WHITE)
