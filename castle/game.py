from typing import List
from .board import Board
from .piece import Piece


class Game:
    def __init__(self):
        self.board = Board()
        self.pieces: List[Piece] = None
        self.place_pieces_for_new_game()

    def place_pieces_for_new_game(self):
        self.board.place_piece(Piece.ROOK, 'a1')
