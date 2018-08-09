from typing import Tuple, List, Set, Union
import random

from castle.piece import Color
from castle.board import Board
from castle.square import Square
from castle.move import Move


class Player:
    def __init__(self, color: Color):
        self.color = color

    def play_move(self, board: Board) -> Union[str, Move]:
        raise NotImplementedError('subclass responsibility')


class HumanPlayer(Player):
    def play_move(self, board: Board) -> str:
        # human player's move consists of asking the user for a move in chess notation
        player_move_str = input(f'{self.color.name.title()}\'s move: ')
        return player_move_str


class RandomPlayer(Player):
    def play_move(self, board: Board) -> Move:
        possible_moves: List[Tuple[Square, Set[Square]]] = []
        for square in board.squares_matching_filter(color=self.color):
            moves = board.get_moves(square)
            if len(moves):
                possible_moves.append((square, moves))
        # pick a random valid move
        source, moves = random.choice(possible_moves)
        dest = random.sample(moves, 1)[0]

        move = Move(self.color, f'({source}->{dest})')
        move.from_square = source
        move.to_square = dest
        return move
