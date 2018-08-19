import unittest

import castle
from castle import Game, Board, Piece, PieceType, Color, InvalidChessNotationError, PlayerType, MoveParser, FenGameConstructor


class GameTests(unittest.TestCase):
    def check_contains_piece(self, game: Game, square_notation: str, piece_type: PieceType, piece_color: Color):
        square = game.board.square_from_notation(square_notation)
        self.assertEqual(piece_type, square.occupant.type)
        self.assertEqual(piece_color, square.occupant.color)

    def test_simple(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)
        move = castle.MoveParser.parse_move(g, 'e4')
        self.assertEqual('e2', move.from_square.notation())
        self.assertEqual('e4', move.to_square.notation())

        # 1. e4 e5 2. Bd3
        g.apply_notation('e4')
        g.apply_notation('e5')
        move = castle.MoveParser.parse_move(g, 'Bd3')
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

        # only way out of check is for pawn to capture queen
        legal_moves = g.get_all_legal_moves(Color.WHITE)
        self.assertEqual(len(legal_moves), 1)
        self.assertEqual(MoveParser.parse_move(g, 'fg2'), legal_moves.pop())

        # capture the queen
        g.apply_notation('fg2')
        # black captures pawn with bishop
        g.apply_notation('Bxg2')

        # now, white king is in check again by threat of black's g2 bishop
        # only move is to capture bishop
        legal_moves = g.get_all_legal_moves(Color.WHITE)
        self.assertEqual(len(legal_moves), 1)
        self.assertEqual(MoveParser.parse_move(g, 'Kxg2'), legal_moves.pop())

    def test_white_kingside_castle(self):
        g = castle.Game(PlayerType.HUMAN, PlayerType.HUMAN)

        # can't castle while obstructed
        self.assertFalse(g.can_castle(Color.WHITE, True))
        self.assertFalse(g.can_castle(Color.WHITE, False))

        g.apply_notation('e4')
        g.apply_notation('e5')
        g.apply_notation('Nf3')
        g.apply_notation('a5')
        g.apply_notation('Be2')
        g.apply_notation('b5')
        # white is now ready to kingside castle
        g.apply_notation('O-O')

        castled_king_square = g.board.square_from_notation('g1')
        self.assertIsNotNone(castled_king_square.occupant)
        self.assertTrue(castled_king_square.occupant.color == Color.WHITE)
        self.assertTrue(castled_king_square.occupant.type == PieceType.KING)

        castled_rook_square = g.board.square_from_notation('f1')
        self.assertIsNotNone(castled_rook_square.occupant)
        self.assertTrue(castled_rook_square.occupant.color == Color.WHITE)
        self.assertTrue(castled_rook_square.occupant.type == PieceType.ROOK)

        # can't castle twice
        self.assertFalse(g.can_castle(Color.WHITE, True))
        self.assertFalse(g.can_castle(Color.WHITE, False))

    def test_black_queenside_castle(self):
        g = FenGameConstructor('r3kbnr/ppp1pppp/n2q4/3p1b2/2PPPP2/8/PP4PP/RNBQKBNR b KQkq - 0 0').game
        self.assertTrue(g.can_black_castle_long)
        self.assertTrue(g.can_black_castle_short)
        self.assertTrue(g.can_castle(Color.BLACK, False))
        self.assertFalse(g.can_castle(Color.BLACK, True))

        # black is now ready to queenside castle
        g.apply_notation('O-O-O')

        castled_king_square = g.board.square_from_notation('c8')
        self.assertIsNotNone(castled_king_square.occupant)
        self.assertTrue(castled_king_square.occupant.color == Color.BLACK)
        self.assertTrue(castled_king_square.occupant.type == PieceType.KING)

        castled_rook_square = g.board.square_from_notation('d8')
        self.assertIsNotNone(castled_rook_square.occupant)
        self.assertTrue(castled_rook_square.occupant.color == Color.BLACK)
        self.assertTrue(castled_rook_square.occupant.type == PieceType.ROOK)

        # can't castle twice
        self.assertFalse(g.can_castle(Color.BLACK, True))
        self.assertFalse(g.can_castle(Color.BLACK, False))

    def test_king_moves(self):
        from castle import MoveParser
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.board.clear()
        # obstructed king with threat of check
        board = g.board
        board.place_piece(Piece(PieceType.KING, Color.WHITE), 'h1')
        board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'h2')
        board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'h3')
        self.assertEqual(
            {
                MoveParser.parse_move(g, 'Kg2'),
                MoveParser.parse_move(g, 'Kg1'),
            },
            g.get_all_legal_moves(Color.WHITE)
        )

        # obstructed king without threat of check
        g.board.clear()
        board.place_piece(Piece(PieceType.KING, Color.WHITE), 'h1')
        board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'h2')
        self.assertEqual(
            {
                MoveParser.parse_move(g, 'Kg2'),
                MoveParser.parse_move(g, 'Kg1'),
                MoveParser.parse_move(g, 'Kh2'),
            },
            g.get_all_legal_moves(Color.WHITE)
        )

        # unobstructed king
        g.board.clear()
        board.place_piece(Piece(PieceType.KING, Color.BLACK), 'e4')
        self.assertEqual(
            {
                board.square_from_notation('d5'),
                board.square_from_notation('e5'),
                board.square_from_notation('d4'),
                board.square_from_notation('f5'),
                board.square_from_notation('d3'),
                board.square_from_notation('f4'),
                board.square_from_notation('e3'),
                board.square_from_notation('f3'),
            },
            board.get_moves(board.square_from_notation('e4'))
        )
