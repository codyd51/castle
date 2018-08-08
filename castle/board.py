from typing import List
from castle.square import Square
from castle.piece import PieceType, Piece


class InvalidChessNotationError(Exception):
    pass


class Board:
    def __init__(self):
        self.squares: List[List[Square]] = Board.construct_squares()

    @classmethod
    def construct_squares(cls) -> List[List[Square]]:
        board: List[List[Square]] = []
        for rank in range(8):
            board.append([])
            for file in range(8):
                square = Square(file, rank)
                board[rank].append(square)
        return board

    def place_piece(self, piece: Piece, location: str) -> None:
        square = self.square_from_notation(location)
        square.occupant = piece

    def square_from_notation(self, location: str) -> Square:
        letter = location[0]
        number = location[1]
        # sanity check
        if letter < 'a' or letter > 'h':
            raise InvalidChessNotationError(f'{location}')
        if not number.isnumeric():
            raise InvalidChessNotationError(f'{location}')

        file = ord(letter) - ord('a')
        rank = int(location[1]) - 1

        if file < 0 or file > 7 or rank < 0 or rank > 7:
            raise InvalidChessNotationError(f'{location}')
        return self.squares[file][rank]

