from typing import List
from .square import Square
from .piece import Piece


class Board:
    def __init__(self):
        self.squares: List[List[Square]] = Board.construct_squares()

    @classmethod
    def construct_squares(cls) -> List[List[Square]]:
        board: List[List[Square]] = []
        for rank in range(8):
            board.append([])
            for file in range(8):
                square = Square(rank, file)
                board[rank].append(square)
        return board

    def place_piece(self, piece: Piece, location: str) -> None:
        square = self.square_from_notation(location)
        square.occupant = piece

    def square_from_notation(self, location: str):
        letter = location[0]
        # sanity check
        if letter < 'a' or letter > 'h':
            raise RuntimeError(f'Invalid chess notation: {location}')
        file = int(location[1])
        if file < 1 or file > 8:
            raise RuntimeError(f'Invalid chess notation: {location}')
        rank = ord(letter) - ord('a')
        return self.squares[rank][file]


b = Board()
print(b.square_from_notation('a3'))
