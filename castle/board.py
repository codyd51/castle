from typing import List, Set, Optional
from castle.square import Square
from castle.piece import PieceType, Piece, Color


class InvalidChessNotationError(Exception):
    pass


class Board:
    def __init__(self):
        self._squares: List[List[Square]] = Board.construct_squares()

    @classmethod
    def construct_squares(cls) -> List[List[Square]]:
        board: List[List[Square]] = []
        for rank in range(8):
            board.append([])
            for file in range(8):
                square = Square(rank, file)
                board[rank].append(square)
        return board

    def get_moves(self, square: Square) -> Set[Square]:
        if square.occupant.type is PieceType.PAWN:
            return self._get_pawn_moves(square)
        elif square.occupant.type is PieceType.KNIGHT:
            return self._get_knight_moves(square)
        elif square.occupant.type is PieceType.BISHOP:
            return self._get_bishop_moves(square)
        elif square.occupant.type is PieceType.ROOK:
            return self._get_rook_moves(square)
        elif square.occupant.type is PieceType.QUEEN:
            pass
        elif square.occupant.type is PieceType.KING:
            pass

    def _get_pawn_moves(self, square: Square) -> Set[Square]:
        """
        :param square: the origin of the bishop
        :return: all possible squares the bishop could move to in the current board state
        """
        moves: Set[Square] = set()
        if square.occupant.color is Color.WHITE:
            forward = 1
            first_rank = 1
        else:
            forward = -1
            first_rank = 6

        # Moves forward
        if self._squares[square.rank + forward][square.file].occupant is None:
            moves.add(self._squares[square.rank + forward][square.file])
            # Special case in pawn movement, where they can advance for two spaces if they are on their starting row
            if square.rank == first_rank and self._squares[first_rank + 2 * forward][square.file].occupant is None:
                moves.add(self._squares[first_rank + 2 * forward][square.file])

        # Left diagonal captures
        if square.file == 0:
            token = None
        else:
            token = self._squares[square.rank + forward][square.file - 1]
        if token and token.occupant and token.occupant.color != square.occupant.color:
            moves.add(token)

        # Right diagonal captures
        if square.file == 7:
            token = None
        else:
            token = self._squares[square.rank + forward][square.file + 1]
        if token and token.occupant and token.occupant.color != square.occupant.color:
            moves.add(token)
        return moves

    def _get_knight_moves(self, square: Square) -> Set[Square]:
        """
        :param square: the origin of the knight
        :return: all possible squares the knight could move to in the current board state
        """
        moves: Set[Square] = set()
        # Moves upwards
        if square.rank <= 5:
            if square.file >= 1:
                token = self._squares[square.rank + 2][square.file - 1]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)
            if square.file <= 6:
                token = self._squares[square.rank + 2][square.file + 1]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)

        # Moves downwards
        if square.rank >= 2:
            if square.file >= 1:
                token = self._squares[square.rank - 2][square.file - 1]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)
            if square.file <= 6:
                token = self._squares[square.rank - 2][square.file + 1]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)

        # Moves to the left
        if square.file >= 2:
            if square.rank >= 1:
                token = self._squares[square.rank - 1][square.file - 2]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)
            if square.rank <= 6:
                token = self._squares[square.rank + 1][square.file - 2]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)

        # Moves to the right
        if square.file <= 5:
            if square.rank >= 1:
                token = self._squares[square.rank - 1][square.file + 2]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)
            if square.rank <= 6:
                token = self._squares[square.rank + 1][square.file + 2]
                if not (token.occupant and token.occupant.color is square.occupant.color):
                    moves.add(token)
        return moves

    def _get_bishop_moves(self, square: Square) -> Set[Square]:
        """
        :param square: the origin of the bishop
        :return: all possible _squares the bishop could move to in the current board state
        """
        moves: Set[Square] = set()
        # moves to the upper-left
        for i in range(1, 8):
            if square.file - i >= 0 and square.rank + i <= 7:
                token: Square = self._squares[square.rank + i][square.file - i]
            else:
                break
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves to the bottom-left
        for i in range(1, 8):
            if square.file - i >= 0 and square.rank - i >= 0:
                token: Square = self._squares[square.rank - i][square.file - i]
            else:
                break
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves to the upper-right
        for i in range(1, 8):
            if square.file + i <= 7 and square.rank + i <= 7:
                token: Square = self._squares[square.rank + i][square.file + i]
            else:
                break
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves to the bottom-right
        for i in range(1, 8):
            if square.file + i <= 7 and square.rank - i >= 0:
                token: Square = self._squares[square.rank - i][square.file + i]
            else:
                break
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        return moves

    def _get_rook_moves(self, square: Square) -> Set[Square]:
        """
        :param square: the origin of the rook
        :return: all possible _squares the rook could move to in the current board state
        """
        moves: Set[Square] = set()
        # moves to the left
        for i in range(square.file - 1, -1, -1):
            token: Square = self._squares[square.rank][i]
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves to the right
        for i in range(square.file + 1, 8):
            token: Square = self._squares[square.rank][i]
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves up
        for i in range(square.rank + 1, 8):
            token: Square = self._squares[i][square.file]
            if token.occupant is None:
                moves.add(token)
            elif token.occupant.color is not square.occupant.color:
                moves.add(token)
                break
            else:
                break
        # moves down
        for i in range(square.rank - 1, -1, -1):
            token: Square = self._squares[i][square.file]
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

    def move_piece_to_square(self, from_square: Square, to_square: Square) -> None:
        if to_square.occupant:
            raise RuntimeError(f'is this a capture? {from_square} {to_square}')
        to_square.occupant = from_square.occupant
        from_square.occupant = None
        # TODO(PT): test this method
        # TODO(PT): this should also update defenders and attackers fields

    def move_piece_to_location(self, from_square: Square, location: str) -> None:
        # TODO(PT): test this method
        dest_square = self.square_from_notation(location)
        self.move_piece_to_square(from_square, dest_square)

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
        return self._squares[rank][file]

    def piece_from_notation(self, location: str) -> Optional[Piece]:
        """
        :param location: location of a square written in chess notation
        :return: Piece which is occupying the given square, or None of no occupant exists
        """
        return self.square_from_notation(location).occupant

    def pretty_print(self):
        def pretty_print_piece(piece: Optional[Piece]):
            if not piece:
                print('_', end='')
                return
            symbols = {
                PieceType.ROOK:     ('♖', '♜'),
                PieceType.KNIGHT:   ('♘', '♞'),
                PieceType.BISHOP:   ('♗', '♝'),
                PieceType.QUEEN:    ('♕', '♛'),
                PieceType.KING:     ('♔', '♚'),
                PieceType.PAWN:     ('♙', '♟')
            }
            idx = 0 if piece.color == Color.WHITE else 1
            symbol = symbols[piece.type][idx]
            print(symbol, end='')

        print('_________________')
        for rank in self._squares[::-1]:
            print('|', end='')
            for square in rank:
                pretty_print_piece(square.occupant)
                print('|', end='')
            print()
        print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    def squares_all(self):
        for rank in self._squares:
            for square in rank:
                yield square
        raise StopIteration

    def squares_occupied(self):
        for square in self.squares_all():
            if square.occupant:
                yield square
        raise StopIteration

    def squares_occupied_white(self):
        for square in self.squares_occupied():
            if square.occupant.color == Color.WHITE:
                yield square
        raise StopIteration

    def squares_occupied_black(self):
        for square in self.squares_occupied():
            if square.occupant.color == Color.BLACK:
                yield square
        raise StopIteration

    def squares_occupied_of_type(self, type: PieceType, color: Color):
        for square in self.squares_occupied():
            if square.occupant.type == type and square.occupant.color == color:
                yield square
        raise StopIteration

    def squares_matching_filter(self,
                                type: Optional[PieceType] = None,
                                color: Optional[Color] = None,
                                rank: Optional[str] = None,
                                file: Optional[str] = None):
        for square in self.squares_all():
            is_match = True
            if type and square.occupant.type != type:
                is_match = False
            if color and square.occupant.color != color:
                is_match = False
            if rank and square.rank != rank:
                is_match = False
            if file and square.file != file:
                is_match = False
            if is_match:
                yield square
        raise StopIteration
