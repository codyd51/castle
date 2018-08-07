from .piece import Piece
from typing import List


class Square:
    def __init__(self, rank: int, file: int):
        rank_values = 'abcdefgh'
        self.rank: int = rank_values[rank]
        self.file: int = file
        self.occupant: Piece = None
        self.white_defenders: List[Square] = []
        self.black_defenders: List[Square] = []

    def __repr__(self):
        return f'{self.rank}{self.file}'
    