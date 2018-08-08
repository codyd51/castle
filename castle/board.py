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

    def get_moves(self, square: Square):
        if square.occupant.type is PieceType.PAWN:
            pass
        elif square.occupant.type is PieceType.KNIGHT:
            pass
        elif square.occupant.type is PieceType.BISHOP:
            pass
        elif square.occupant.type is PieceType.ROOK:
            return self._get_rook_moves(square)
        elif square.occupant.type is PieceType.QUEEN:
            pass
        elif square.occupant.type is PieceType.KING:
            pass

    def _get_rook_moves(self, square: Square):
        """
        :param square: the origin of the rook
        :return: all possible squares the rook could move to in the current board state
        """
        moves: List[Square] = []
        # moves to the left
        for i in range(square.file - 1, -1, -1):
            if self.squares[square.rank][i].occupant is None:
                moves.append(self.squares[square.rank][i])
            else:
                break
        # moves to the right
        for i in range(square.file + 1, 8):
            if self.squares[square.rank][i].occupant is None:
                moves.append(self.squares[square.rank][i])
            else:
                break
        # moves up
        for i in range(square.rank + 1, 8):
            if self.squares[i][square.file].occupant is None:
                moves.append(self.squares[i][square.file])
            else:
                break
        # moves down
        for i in range(square.rank - 1, -1, -1):
            if self.squares[i][square.file].occupant is None:
                moves.append(self.squares[i][square.file])
            else:
                break
        return moves

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
