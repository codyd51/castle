from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Piece:
    def __init__(self, type: PieceType, color: Color):
        self.type = type
        self.color = color

    def __repr__(self):
        return f'<{self.color.value} {self.type.name}>'

    @property
    def value(self):
        if self.type == PieceType.PAWN:
            return 1
        elif self.type == PieceType.KNIGHT or self.type == PieceType.BISHOP:
            return 3
        elif self.type == PieceType.ROOK:
            return 5
        elif self.type == PieceType.QUEEN:
            return 9
        return 999
