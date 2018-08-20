import unittest

import castle
from castle import Game, Board, Piece, PieceType, Color, InvalidChessNotationError, PlayerType, MoveParser, FenGameConstructor
from typing import List


class PerftTests(unittest.TestCase):
    def run_perft(self, game_state: str, correct_perft: List[int]):
        f = FenGameConstructor(game_state)
        f.game.pretty_print()
        actual_perft = f.game.print_perft(len(correct_perft))
        self.assertEqual(correct_perft, actual_perft)

    def test_perft_standard(self):
        self.run_perft(
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -',
            [
                20,
                400,
                8902,
                197281,
                4865609
            ]
        )

    def test_perft1(self):
        self.run_perft(
            '8/5p2/8/2k3P1/p3K3/8/1P6/8 b - -',
            [
                9,
                85,
                795,
                7658
            ]
        )

    def test_perft2(self):
        self.run_perft(
            '8/p7/8/1P6/K1k3p1/6P1/7P/8 w - -',
            [
                5,
                39,
                237,
                2002
            ]
        )

    def test_perft3(self):
        self.run_perft(
            'r3k2r/p6p/8/B7/1pp1p3/3b4/P6P/R3K2R w KQkq -',
            [
                17,
                341,
                6666
            ]
        )

    def test_perft4(self):
        self.run_perft(
            'r3k2r/p6p/8/B7/1pp1p3/3b4/P6P/R3K2R w KQkq -',
            [
                17,
                341,
                6666
            ]
        )

    def test_perft5(self):
        self.run_perft(
            'r3k2r/pb3p2/5npp/n2p4/1p1PPB2/6P1/P2N1PBP/R3K2R b KQkq -',
            [
                29,
                953,
                27990
            ]
        )
