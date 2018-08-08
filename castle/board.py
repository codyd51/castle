from typing import List, Set
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
                square = Square(rank, file)
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

    def _get_bishop_moves(self, square: Square) -> Set[Square]:
        pass

    def _get_rook_moves(self, square: Square) -> Set[Square]:
        """
        :param square: the origin of the rook
        :return: all possible squares the rook could move to in the current board state
        """
        moves: Set[Square] = set()
        # moves to the left
        for i in range(square.file - 1, -1, -1):
            token: Square = self.squares[square.rank][i]
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves to the right
        for i in range(square.file + 1, 8):
            token: Square = self.squares[square.rank][i]
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves up
        for i in range(square.rank + 1, 8):
            token: Square = self.squares[i][square.file]
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves down
        for i in range(square.rank - 1, -1, -1):
            token: Square = self.squares[i][square.file]
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
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
        return self.squares[rank][file]
