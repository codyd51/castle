from typing import List
from .square import Square


class Board:
    def __init__(self):
        self.squares: List[List[Square]] = Board.construct_squares()
        self.place_startingpieces()

    @classmethod
    def construct_squares(cls) -> List[List[Square]]:
        board: List[List[Square]] = []
        for rank in range(8):
            for file in range(8):
                square = Square(rank, file)
                board[rank][file] = square
        return board
