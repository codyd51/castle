import unittest

import castle
from castle import Game, Board, Piece, PieceType, Color, InvalidChessNotationError, PlayerType, MoveParser, FenGameConstructor


class CastleTests(unittest.TestCase):
    def test_can_short_castle(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 e5 2. Bd3 d5 3. Nf3 f5 4. a4 g5')
        self.assertTrue(g.can_castle(Color.WHITE, True))
        self.assertFalse(g.can_castle(Color.WHITE, False))
        self.assertFalse(g.can_castle(Color.BLACK, True))
        self.assertFalse(g.can_castle(Color.BLACK, False))

    def test_can_long_castle(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. d4 d5 2. e4 e5 3. Bf4 Qd7 4. Qg4 c6 5. Nc3')
        self.assertTrue(g.can_castle(Color.WHITE, False))
        self.assertFalse(g.can_castle(Color.WHITE, True))
        self.assertFalse(g.can_castle(Color.BLACK, True))
        self.assertFalse(g.can_castle(Color.BLACK, False))

    def test_castle_after_king_movement(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 e5 2. Bd3 d5 3. Nf3 f5 4. Kf1 g5 5. Ke1 c5')
        # white has moved king
        self.assertFalse(g.can_castle(Color.WHITE, True))
        # test all the others just to be safe
        self.assertFalse(g.can_castle(Color.WHITE, False))
        self.assertFalse(g.can_castle(Color.BLACK, True))
        self.assertFalse(g.can_castle(Color.BLACK, False))

    def test_castle_after_rook_movement(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 e5 2. Bd3 d5 3. Nf3 f5 4. Rf1 g5 5. Rh1 c5')
        # white has moved rook
        self.assertFalse(g.can_castle(Color.WHITE, True))
        # test all the others just to be safe
        self.assertFalse(g.can_castle(Color.WHITE, False))
        self.assertFalse(g.can_castle(Color.BLACK, True))
        self.assertFalse(g.can_castle(Color.BLACK, False))

    def test_castle_obstructed(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        self.assertFalse(g.can_castle(Color.WHITE, True))
        self.assertFalse(g.can_castle(Color.WHITE, False))
        self.assertFalse(g.can_castle(Color.BLACK, True))
        self.assertFalse(g.can_castle(Color.BLACK, False))

    def test_can_castle_in_check(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 e5 2. d4 f5 3. Bd3 d5 4. Nf3 c5 5. c4 ')
        # can castle now
        self.assertTrue(g.can_castle(Color.WHITE, True))
        # put white in check
        g.apply_notation('Qa5')
        # can't castle out of check
        self.assertFalse(g.can_castle(Color.WHITE, True))

    def test_can_castle_through_check(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 b6 2. Nf3 e5 3. g3 d5 4. Bg2 ')
        # can castle now
        self.assertTrue(g.can_castle(Color.WHITE, True))
        # attack f1, which the king would pass through
        g.apply_notation('Ba6')
        # can't castle through check
        self.assertFalse(g.can_castle(Color.WHITE, True))

    def test_can_castle_into_check(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. f4 e5 2. Nh3 g5 3. g4 f5 4. Bg2 Bc5')
        # can castle now
        self.assertTrue(g.can_castle(Color.WHITE, True))
        # attack g1, which the king moves to
        g.apply_notation('Bc5')
        # can't castle through check
        self.assertFalse(g.can_castle(Color.WHITE, True))
