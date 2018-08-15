import unittest

import castle
from castle import Game, Board, Piece, PieceType, Color, InvalidChessNotationError, PlayerType, MoveParser


class GameTests(unittest.TestCase):
    def check_contains_piece(self, game: Game, square_notation: str, piece_type: PieceType, piece_color: Color):
        square = game.board.square_from_notation(square_notation)
        self.assertEqual(piece_type, square.occupant.type)
        self.assertEqual(piece_color, square.occupant.color)

    def test_simple(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)
        move = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'e4')
        self.assertEqual('e2', move.from_square.notation())
        self.assertEqual('e4', move.to_square.notation())

        # 1. e4 e5 2. Bd3
        g.apply_notation('e4')
        move = castle.MoveParser.parse_move(g.board, castle.Color.WHITE, 'Bd3')
        self.assertEqual('f1', move.from_square.notation())
        self.assertEqual('d3', move.to_square.notation())

    def test_bishop_capture(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_notation('e4')
        g.apply_notation('e5')
        g.apply_notation('d4')
        g.apply_notation('a6')
        g.apply_notation('Bxa6')
        self.check_contains_piece(g, 'a6', PieceType.BISHOP, Color.WHITE)

    def test_pawn_capture(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_notation('e4')
        g.apply_notation('f5')
        # TODO(PT): once MoveParser returns a Move object, this should verify a capture was indicated
        g.apply_notation('exf5')
        self.check_contains_piece(g, 'f5', PieceType.PAWN, Color.WHITE)

    def test_knight_movement(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_notation('e4')
        g.apply_notation('e5')
        g.apply_notation('Ne2')
        self.check_contains_piece(g, 'e2', PieceType.KNIGHT, Color.WHITE)

    def test_ambiguous_knight_movement(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_notation('e4')
        g.apply_notation('e5')
        g.apply_notation('Ne2')
        g.apply_notation('f6')
        with self.assertRaises(InvalidChessNotationError):
            g.apply_notation('Nc3')

        g.apply_notation('Nec3')
        self.check_contains_piece(g, 'c3', PieceType.KNIGHT, Color.WHITE)

    def test_moves_in_check(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.board.clear()
        g.board.place_piece(Piece(PieceType.KING, Color.WHITE), 'h1')
        g.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'f1')
        g.board.place_piece(Piece(PieceType.QUEEN, Color.BLACK), 'g2')
        g.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'f3')
        g.board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'g4')
        g.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'e3')
        g.board.pretty_print()

        # only way out of check is for pawn to capture queen
        legal_moves = g.board.get_all_legal_moves(Color.WHITE)
        self.assertEqual(len(legal_moves), 1)
        self.assertEqual(MoveParser.parse_move(g.board, Color.WHITE, 'fg2'), legal_moves.pop())

        # capture the queen
        g.apply_notation('fg2')
        # black captures pawn with bishop
        g.apply_notation('Bxg2')

        # now, white king is in check again by threat of black's g2 bishop
        # only move is to capture bishop
        legal_moves = g.board.get_all_legal_moves(Color.WHITE)
        self.assertEqual(len(legal_moves), 1)
        self.assertEqual(MoveParser.parse_move(g.board, Color.WHITE, 'Kxg2'), legal_moves.pop())


