from typing import List, Optional
from castle.square import Square
from castle.piece import PieceType, Piece, Color


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
                square = Square(rank, file)
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
        return self.squares[rank][file]

    def pretty_print(self):
        def pretty_print_piece(piece: Optional[Piece]):
            if not piece:
                print('_', end='')
                return
            acronyms = {
                PieceType.ROOK:     'R',
                PieceType.KNIGHT:   'N',
                PieceType.BISHOP:   'B',
                PieceType.QUEEN:    'Q',
                PieceType.KING:     'K',
                PieceType.PAWN:     'P'
            }
            acronym = acronyms[piece.type]
            if piece.color == Color.BLACK:
                acronym = acronym.lower()
            print(acronym, end='')

        print('_________________')
        for rank in self.squares[::-1]:
            print('|', end='')
            for square in rank:
                pretty_print_piece(square.occupant)
                print('|', end='')
            print()
