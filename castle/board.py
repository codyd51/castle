from typing import List, Set, Optional
from castle.square import Square
from castle.piece import PieceType, Piece, Color
from castle.move import Move, MoveParser


class InvalidChessNotationError(Exception):
    pass


class Board:
    def __init__(self):
        self._squares: List[List[Square]] = Board.construct_squares()

    def clear(self):
        """Remove all occupants from the board. Typically used for testing purposes.
        """
        for square in self.squares_occupied():
            square.occupant = None

    @classmethod
    def construct_squares(cls) -> List[List[Square]]:
        board: List[List[Square]] = []
        for rank in range(8):
            board.append([])
            for file in range(8):
                square = Square(rank, file)
                board[rank].append(square)
        return board

    def copy(self) -> 'Board':
        clone = Board()
        for square, copy_square in list(zip(self.squares_all(), clone.squares_all())):
            if square.occupant:
                copy_square.occupant = Piece(square.occupant.type, square.occupant.color)
        return clone

    def copy_move(self, move: Move) -> Move:
        from_square = self.square_from_notation(move.from_square.notation())
        to_square = self.square_from_notation(move.to_square.notation())
        return MoveParser.move_from_squares(from_square, to_square)

    def get_all_legal_moves(self, color: Color) -> Set[Move]:
        """Returns a set of all legal Moves from the current board state, respecting rules like check.
        """
        all_moves = self._get_all_moves(color)
        legal_moves = all_moves.copy()
        # if one player is in check, restrict their legal moves to the ones that would get them out of check
        if self.is_in_check(color):
            # go through and apply each move to a new Board, and check if player is still in check
            for move in all_moves:
                new_board = self.copy()
                copied_move = new_board.copy_move(move)
                # TODO(PT): add a Board.apply_move(move: Move)
                new_board.move_piece_to_square(copied_move.from_square, copied_move.to_square)
                if new_board.is_in_check(color):
                    # throw away this move because it doesn't get us out of check
                    legal_moves.remove(move)
        if not len(legal_moves):
            # there are no moves that would get us out of check
            raise RuntimeError(f'checkmate')
        return legal_moves

    def _get_all_moves(self, color: Color) -> Set[Move]:
        """Returns a set of all possible Moves from the current board state. Does not respect check!
        """
        moves: Set[Move] = set()
        movable_squares = self.squares_matching_filter(color=color)
        for source in movable_squares:
            moves_from_source = self.get_moves(source)
            # make a move from each of these
            # TODO(PT): perhaps get_moves() should return a Move?
            for dest in moves_from_source:
                move = MoveParser.move_from_squares(source, dest)
                moves.add(move)
        return moves

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
            return self._get_queen_moves(square)
        elif square.occupant.type is PieceType.KING:
            return self._get_king_moves(square)

    def _get_pawn_moves(self, square: Square) -> Set[Square]:
        """
        :param square: the origin of the pawn
        :return: all possible squares the pawn could move to in the current board state
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

    def _get_queen_moves(self, square: Square) -> Set[Square]:
        """
        :param square: the origin of the queen
        :return: all possible _squares the queen could move to in the current board state
        """
        return self._get_bishop_moves(square) | self._get_rook_moves(square)

    def _get_king_moves(self, square: Square) -> Set[Square]:
        # TODO(PT): should all movement methods assert the occupant?
        valid_adjacent_squares = set()
        # get all the squares surrounding this one
        for x in range(square.rank - 1, square.rank + 2):
            for y in range(square.file - 1, square.file + 2):
                try:
                    # if this square is off the board, this call will raise an exception
                    s = self.square_from_coord(x, y)
                    if not s.occupant or s.occupant.color != square.occupant.color:
                        valid_adjacent_squares.add(s)
                except InvalidChessNotationError:
                    continue
        return valid_adjacent_squares

    def place_piece(self, piece: Piece, location: str) -> None:
        square = self.square_from_notation(location)
        square.occupant = piece

    def move_piece_to_square(self, from_square: Square, to_square: Square) -> None:
        # TODO(PT): test this method
        # TODO(PT): this should also update defenders and attackers fields
        if not from_square.occupant:
            raise RuntimeError(f'Can\'t move {from_square} to {to_square}. No piece on {from_square}.')
        to_square.occupant = from_square.occupant
        from_square.occupant = None

        # is this a pawn promotion?
        if to_square.occupant.type == PieceType.PAWN:
            top_rank = 7 if to_square.occupant.color == Color.WHITE else 0
            if to_square.rank == top_rank:
                print(f'Promoting pawn at {to_square} to Queen. Flesh me out?')
                to_square.occupant = Piece(PieceType.QUEEN, to_square.occupant.color)

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

        return self.square_from_coord(rank, file)

    def square_from_coord(self, rank: int, file: int) -> Square:
        if file < 0 or file > 7 or rank < 0 or rank > 7:
            raise InvalidChessNotationError(f'({rank},{file})')
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

    def squares_occupied(self):
        for square in self.squares_all():
            if square.occupant:
                yield square

    def squares_matching_filter(self,
                                type: Optional[PieceType] = None,
                                color: Optional[Color] = None,
                                rank: Optional[int] = None,
                                file: Optional[int] = None,
                                rank_str: Optional[str] = None,
                                file_str: Optional[str] = None,
                                can_reach_square: Optional[Square] = None):
        for square in self.squares_occupied():
            is_match = True
            if type and square.occupant.type != type:
                is_match = False
            if color and square.occupant.color != color:
                is_match = False
            if rank and square.rank != rank:
                is_match = False
            if file and square.file != file:
                is_match = False
            if rank_str and rank_str != str(square.rank):
                is_match = False
            if file_str and file_str != Square.index_to_file(square.file):
                is_match = False
            if can_reach_square:
                moves = self.get_moves(square)
                if can_reach_square not in moves:
                    is_match = False

            if is_match:
                yield square

    def is_in_check(self, color: Color) -> bool:
        # TODO(PT): test me
        opponent_color = color.opposite()
        opponent_moves = self._get_all_moves(opponent_color)
        # look at all the moves for the opposite player's next turn, and see if one of them includes a king capture
        for move in opponent_moves:
            if not move.to_square.occupant:
                continue
            if move.to_square.occupant.type == PieceType.KING:
                # the opponent can capture our king on the next move, we are in check
                return True
        return False
