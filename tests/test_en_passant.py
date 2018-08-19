import unittest

import castle
from castle import Game, Board, Piece, PieceType, Color, InvalidChessNotationError, PlayerType, MoveParser, FenGameConstructor, EnPassantMove


class EnPassantTests(unittest.TestCase):
    def test_en_passant_white(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 f5 2. e5 d5 ')
        g.apply_notation('exd6')
        unsafe = g.board.square_from_notation('d5')
        target = g.board.square_from_notation('d6')
        attack = g.board.square_from_notation('e5')

        # attacker moved from here
        self.assertIsNone(attack.occupant)
        # to here
        self.assertEqual(Piece(PieceType.PAWN, Color.WHITE), target.occupant)
        # unsafe square was captured
        self.assertIsNone(unsafe.occupant)

    def test_en_passant_black(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. a4 d5 2. c4 d4 3. e4 ')
        g.apply_notation('dxe3')
        unsafe = g.board.square_from_notation('e4')
        target = g.board.square_from_notation('e3')
        attack = g.board.square_from_notation('d4')

        # attacker moved from here
        self.assertIsNone(attack.occupant)
        # to here
        self.assertEqual(Piece(PieceType.PAWN, Color.BLACK), target.occupant)
        # unsafe square was captured
        self.assertIsNone(unsafe.occupant)

    def test_en_passant_after_turn_expires(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 f5 2. e5 d5 3. a4 a5 ')
        legal_moves = g.get_all_legal_moves(Color.WHITE)
        for m in legal_moves:
            if type(m) == EnPassantMove:
                self.assert_('En passant not allowed here')

    def test_en_passant_on_correct_turn(self):
        g = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        g.apply_record('1. e4 f5 2. e5 d5 ')
        legal_moves = g.get_all_legal_moves(Color.WHITE)
        found = False
        for m in legal_moves:
            if type(m) == EnPassantMove:
                found = True
        if not found:
            self.assert_('En passant not found in legal moves')

