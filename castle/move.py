from castle.piece import Piece, PieceType, Color
from castle.square import Square
from typing import List


class InvalidMoveError(Exception):
    pass


class Move:
    def __init__(self, color: Color, notation: str = None):
        self.color = color
        self.notation = notation
        self.from_square: Square = None
        self.to_square: Square = None
        self.is_capture = False
        self.active_piece: Piece = None
        self.captured_piece: Piece = None

    def __eq__(self, other: 'Move'):
        # TODO(PT): test me!
        if self.color != other.color:
            return False
        if self.to_square.notation() != other.to_square.notation():
            return False
        if self.from_square.notation() != other.from_square.notation():
            return False
        # XXX(PT): this does not check the generated notation (since it can vary depending on the source of the Move),
        # or the is_capture flag.
        return True

    def __hash__(self):
        return hash((self.color, self.from_square.notation(), self.to_square.notation()))

    def __repr__(self):
        return f'({self.from_square.notation()}{self.to_square.notation()})'

    def undo(self, board: 'Board'):
        board.move_piece_to_square(self.to_square, self.from_square)


class MoveParser:
    @classmethod
    def move_from_squares(cls, source: Square, dest: Square) -> Move:
        if not source.occupant:
            raise RuntimeError(f'can\'t move from a square with no occupant {source}')
        move = Move(source.occupant.color)
        move.from_square = source
        move.to_square = dest
        move.active_piece = source.occupant
        if dest.occupant:
            move.is_capture = True
            move.captured_piece = dest.occupant
            if source.occupant.color == dest.occupant.color:
                raise RuntimeError(f'can\'t capture another piece of the same color')
        move.notation = MoveParser.notation_from_move(move)
        return move

    @classmethod
    def notation_from_move(cls, move: Move):
        notation = f''
        notation += PieceType.symbol_from_type(move.from_square.occupant.type)
        notation += Square.index_to_file(move.from_square.file)
        if move.is_capture:
            notation += 'x'
        notation += move.to_square.notation()
        # internally MoveParser will prepend P to pawn moves; clean it up.
        notation = notation.strip('P')
        return notation

    @staticmethod
    def parse_move(board: 'Board', active_color: Color, move_str: str) -> Move:
        """Parses chess notation in the context of the board, and returns the piece which is moving and its destination.
        """
        from castle.board import InvalidChessNotationError
        if not len(move_str):
            raise InvalidChessNotationError('Non-empty chess move required')

        # castle?
        if move_str == CastleMove.KINGSIDE_NOTATION:
            return CastleMove(active_color, True)
        elif move_str == CastleMove.QUEENSIDE_NOTATION:
            return CastleMove(active_color, False)

        move = Move(active_color, move_str)
        # if a pawn is being moved, prepend a P to the notation string so pawn movements are internally
        # consistent with other piece's movement. This is so all pieces can be handled with the same logic.
        if move_str[0].islower():
            move_str = f'P{move_str}'

        # is it a capture? SxDD
        if 'x' in move_str:
            move.is_capture = True
            # TODO(PT): test for Nexd6
            from_square = move_str[:move_str.find('x')]
            to_square_str = move_str[move_str.find('x')+1:]
            move.to_square = board.square_from_notation(to_square_str)
            move.captured_piece = move.to_square.occupant

            from_type = PieceType.type_from_symbol(from_square[0])
            from_file = None
            # if a file is specified, make use of it
            if len(from_square) > 1:
                from_file = from_square[1]
            from_squares = list(board.squares_matching_filter(type=from_type,
                                                              color=active_color,
                                                              file_str=from_file,
                                                              can_reach_square=move.to_square))
            # there should be exactly one source square
            if len(from_squares) != 1:
                # check if this is en passant
                if game.en_passant_eligible():
                    rank = 5 if active_color == Color.WHITE else 4
                    from_square = board.square_from_notation(f'{from_file}{rank}')
                    unsafe_square = board.square_from_notation(f'{Square.index_to_file(move.to_square.file)}{rank}')
                    return EnPassantMove(move.to_square, from_square, unsafe_square)
                else:
                    raise InvalidMoveError(f'{move_str} is ambiguous')

            move.from_square = from_squares[0]
            move.active_piece = move.from_square.occupant
            return move

        # piece type will be the first character
        piece_type = PieceType.type_from_symbol(move_str[0])
        # if the total move is >= 4 characters, then the second character specifies the file of the source piece (Ned6)
        if len(move_str) >= 4:
            from_file = move_str[1]
            move.to_square = board.square_from_notation(move_str[2:])
        else:
            from_file = None
            move.to_square = board.square_from_notation(move_str[1:])

        pieces_fulfilling_source_square_requirements: List[Square] = []
        for square in board.squares_matching_filter(
                color=active_color,
                type=piece_type,
                file_str=from_file,
                can_reach_square=move.to_square):
            # found the piece to move
            pieces_fulfilling_source_square_requirements.append(square)

        # if there were multiple pieces matching all the necessary criteria to perform the provided notation,
        # then the notation is invalid and must contain the source square's file
        if len(pieces_fulfilling_source_square_requirements) > 1:
            raise InvalidChessNotationError(f'Ambiguous move: {move_str}')
        elif len(pieces_fulfilling_source_square_requirements) == 1:
            move.from_square = pieces_fulfilling_source_square_requirements[0]
            move.active_piece = move.from_square.occupant
            return move

        raise InvalidMoveError(move_str)


class CastleMove(Move):
    KINGSIDE_NOTATION = 'O-O'
    QUEENSIDE_NOTATION = 'O-O-O'

    def __init__(self, color: Color, kingside: bool):
        notation = CastleMove.KINGSIDE_NOTATION if kingside else CastleMove.QUEENSIDE_NOTATION
        super(CastleMove, self).__init__(color, notation)
        self.color = color
        self.kingside = kingside

    def __eq__(self, other):
        if type(other) != CastleMove:
            return False
        if self.color != other.color:
            return False
        if self.kingside != other.kingside:
            return False
        return True

    def __hash__(self):
        return hash((self.color, self.kingside))

    def __repr__(self):
        color = self.color.name.title()
        side = 'short' if self.kingside else 'long'
        return f'({color} {side} castle)'

    def apply(self, board: 'Board'):
        king_file = Square.file_to_index('e')
        if self.color == Color.WHITE:
            rank = 0
        else:
            rank = 7
        if self.kingside:
            rook_file = Square.file_to_index('h')
            rook_dest_file = Square.file_to_index('f')
            king_dest_file = Square.file_to_index('g')
        else:
            rook_file = Square.file_to_index('a')
            rook_dest_file = Square.file_to_index('d')
            king_dest_file = Square.file_to_index('c')

        king = board.square_from_coord(rank, king_file)
        rook = board.square_from_coord(rank, rook_file)
        king_dest = board.square_from_coord(rank, king_dest_file)
        rook_dest = board.square_from_coord(rank, rook_dest_file)

        board.move_piece_to_square(rook, rook_dest)
        board.move_piece_to_square(king, king_dest)

    def undo(self, board: 'Board'):
        rank = 0 if self.color == Color.WHITE else 7
        king_orig_file = 4
        king_curr_file = 6 if self.kingside else 2
        king_orig_square = board.square_from_coord(rank, king_orig_file)
        king_curr_square = board.square_from_coord(rank, king_curr_file)

        rook_orig_file = 7 if self.kingside else 0
        rook_curr_file = 5 if self.kingside else 3
        rook_orig_square = board.square_from_coord(rank, rook_orig_file)
        rook_curr_square = board.square_from_coord(rank, rook_curr_file)

        board.move_piece_to_square(king_curr_square, king_orig_square)
        board.move_piece_to_square(rook_curr_square, rook_orig_square)


class EnPassantMove(Move):
    def __init__(self, target_square: Square, attacker: Square, unsafe_square: Square):
        self.target_square = target_square
        self.attacker = attacker
        self.unsafe_square = unsafe_square

        self.active_piece = self.attacker.occupant

        notation = f'{Square.index_to_file(attacker.file)}x{self.target_square.notation()}'
        super(EnPassantMove, self).__init__(self.attacker.occupant.color, notation)

    def __eq__(self, other):
        if self.target_square != other.target_square:
            return False
        if self.attacker != other.attacker:
            return False
        if self.unsafe_square != other.unsafe_square:
            return False
        if self.color != other.color:
            return False
        return True

    def __hash__(self):
        return hash((self.target_square, self.attacker, self.unsafe_square))

    def __repr__(self):
        sup = super(EnPassantMove, self).__repr__()
        return f'e.p. {sup}'

    def apply(self, board: 'Board'):
        board.move_piece_to_square(self.attacker, self.target_square)
        if not self.target_square:
            raise RuntimeError(f'unsafe square for en passant was empty?')
        self.unsafe_square.occupant = None

    def undo(self, board: 'Board'):
        board.move_piece_to_square(self.target_square, self.attacker)
        self.unsafe_square.occupant = Piece(PieceType.PAWN, self.color.opposite())
