from typing import List
from castle.board import Board
from castle.piece import Piece, PieceType, Color


class Game:
    def __init__(self):
        self.board = Board()
        self.pieces: List[Piece] = None
        self.place_pieces_for_new_game()

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
        self.board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'a1')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'b1')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'c1')
        self.board.place_piece(Piece(PieceType.QUEEN, Color.BLACK), 'd1')
        self.board.place_piece(Piece(PieceType.KING, Color.BLACK), 'e1')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'f1')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'g1')
        self.board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'h1')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'a2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'b2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'c2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'd2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'e2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'f2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'g2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'h2')