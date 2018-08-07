from castle.piece import Piece
from typing import List


class Square:
    def __init__(self, rank: int, file: int):

        self.rank: int = rank
        self.file: int = file
        self.occupant: Piece = None
        self.white_defenders: List[Square] = []
        self.black_defenders: List[Square] = []

    def __repr__(self):
        rank_values = 'abcdefgh'
        return f'{rank_values[self.rank]}{self.file}'
