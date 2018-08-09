from castle.piece import Piece
from typing import List


class Square:
    def __init__(self, rank: int, file: int):
        self.rank: int = rank
        self.file: int = file
        self.occupant: Piece = None
        self.white_defenders: List[Square] = []
        self.black_defenders: List[Square] = []

    @staticmethod
    def file_to_index(file: str):
        # TODO(PT): replace usage throughout project with this
        return ord(file) - ord('a')

    def __repr__(self):
        file_values = 'abcdefgh'
        # ranks are 1-indexed
        return f'{file_values[self.file]}{self.rank + 1}'
