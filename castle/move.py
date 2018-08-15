from castle.piece import Piece, PieceType, Color
from castle.square import Square


class InvalidMoveError(Exception):
    pass


class Move:
    def __init__(self, color: Color, notation: str = None):
        self.color = color
        self.notation = notation
        self.from_square: Square = None
        self.to_square: Square = None
        self.is_capture = False

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


class MoveParser:
    @classmethod
    def move_from_squares(cls, source: Square, dest: Square) -> Move:
        if not source.occupant:
            raise RuntimeError(f'can\'t move from a square with no occupant {source}')
        move = Move(source.occupant.color)
        move.from_square = source
        move.to_square = dest
        if dest.occupant:
            move.is_capture = True
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
                raise InvalidMoveError(move_str)
            move.from_square = from_squares[0]
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
        for square in board.squares_matching_filter(type=piece_type, color=active_color, file_str=from_file):
            moves = board.get_moves(square)
            if move.to_square in moves:
                # found the piece to move
                pieces_fulfilling_source_square_requirements.append(square)
        # if there were multiple pieces matching all the necessary criteria to perform the provided notation,
        # then the notation is invalid and must contain the source square's file
        if len(pieces_fulfilling_source_square_requirements) > 1:
            raise InvalidChessNotationError(f'Ambiguous move: {move_str}')
        elif len(pieces_fulfilling_source_square_requirements) == 1:
            move.from_square = pieces_fulfilling_source_square_requirements[0]
            return move

        raise InvalidMoveError(move_str)
