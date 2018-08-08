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
        file_values = 'abcdefgh'
        # ranks are 1-indexed
        return f'{file_values[self.file]}{self.rank + 1}'
