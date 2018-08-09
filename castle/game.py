from typing import List, Tuple
from castle.board import Board, InvalidChessNotationError
from castle.piece import Piece, PieceType, Color
from castle.square import Square


class InvalidMoveError(Exception):
    pass


class MoveParser:
    @staticmethod
    def _find_pawn_for_destination(board: Board, dest_square: str) -> str:
        # the from square is either 1 or 2 squares below the destination square
        rank = int(dest_square[1])
        file = Square.file_to_index(dest_square[0])
        for i in range(1, 3):
            # check if there's a pawn at this square
            possible_source = board.square_from_notation(f'{Square.index_to_file(file)}{rank-i}')
            if possible_source.occupant and possible_source.occupant.type == PieceType.PAWN:
                # found the source piece
                return possible_source.notation()
        raise RuntimeError(f'couldn\'t find pawn that can move to {dest_square}')

    @staticmethod
    def parse_move(board: Board, move: str) -> Tuple[Square, Square]:
        """Parses chess notation in the context of the board, and returns the piece which is moving and its destination.
        """
        # is it a capture? SxDD
        if 'x' in move:
            from_square = move[:move.find('x')]
            to_square = move[move.find('x')+1:]
            print(f'Capture from {from_square} to {to_square}')
        else:
            # is it a pawn move? Pawn moves are only 2 characters long. DD
            if len(move) == 2:
                to_square = move
                from_square = MoveParser._find_pawn_for_destination(board, to_square)
            else:
                raise RuntimeError(f'cant parse {move}')
        return board.square_from_notation(from_square), board.square_from_notation(to_square)


class Game:
    def __init__(self):
        self.board = Board()
        self.pieces: List[Piece] = None
        self.place_pieces_for_new_game()
        self.current_color = Color.WHITE

    def place_pieces_for_new_game(self):
        # white's pieces
        self.board.place_piece(Piece(PieceType.ROOK, Color.WHITE), 'a1')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.WHITE), 'b1')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.WHITE), 'c1')
        self.board.place_piece(Piece(PieceType.QUEEN, Color.WHITE), 'd1')
        self.board.place_piece(Piece(PieceType.KING, Color.WHITE), 'e1')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.WHITE), 'f1')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.WHITE), 'g1')
        self.board.place_piece(Piece(PieceType.ROOK, Color.WHITE), 'h1')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'a2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'b2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'c2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'd2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'e2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'f2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'g2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'h2')

        # black's pieces
        self.board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'a8')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'b8')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'c8')
        self.board.place_piece(Piece(PieceType.QUEEN, Color.BLACK), 'd8')
        self.board.place_piece(Piece(PieceType.KING, Color.BLACK), 'e8')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'f8')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'g8')
        self.board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'h8')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'a7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'b7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'c7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'd7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'e7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'f7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'g7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'h7')

    def play_turn(self):
        while True:
            try:
                self.player_move()
            except InvalidMoveError:
                print('Invalid move.')
            except InvalidChessNotationError:
                print('Invalid notation.')
            break
        self.current_color = Color.WHITE if self.current_color == Color.BLACK else Color.BLACK
        # XXX(PT): for now, a turn always simply consists of performing a move from stdin
        player_move_str = input('Enter a move: ')
        # XXX(PT): this should later be refactored into a separate step for parsing once it's fleshed out
        # check if they're moving a pawn or a named piece
        if player_move_str[0].islower():
            destination = self.board.square_from_notation(player_move_str)
            # player must be moving a pawn
            # loop through every pawn and see if it's possible for it to move to the specified position
            for square in self.board.squares_occupied_of_type(PieceType.PAWN, self.current_color):
                possible_moves = self.board.get_moves(square)
                print(f'Possible {square} {PieceType.PAWN.name} moves: {possible_moves}')
                if destination in possible_moves:
                    # make a move!
                    self.board.move_piece_to_square(square, destination)
                    return
        else:
            piece_type = PieceType.type_from_symbol(player_move_str[0])
            destination_str = player_move_str[1:]
            destination = self.board.square_from_notation(destination_str)
            for square in self.board.squares_occupied_of_type(piece_type, self.current_color):
                possible_moves = self.board.get_moves(square)
                print(f'Possible {square} {piece_type.name} moves: {possible_moves}')
                if destination in possible_moves:
                    self.board.move_piece_to_square(square, destination)
                    return
        raise InvalidMoveError(player_move_str)
