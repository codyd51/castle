from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 8
    KING = 999


class Piece:
    def __init__(self, type: PieceType, color: Color):
        self.type = type
        self.color = color

    def __repr__(self):
        return f'{self.color} {self.type}'
