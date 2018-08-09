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
    def file_to_index(file: str) -> int:
        # TODO(PT): replace usage throughout project with this
        return ord(file) - ord('a')

    @staticmethod
    def index_to_file(idx: int) -> str:
        file_values = 'abcdefgh'
        return file_values[idx]

    def __repr__(self):
        # ranks are 1-indexed
        return f'{Square.index_to_file(self.file)}{self.rank + 1}'
