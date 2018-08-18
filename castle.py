import castle

from typing import Tuple


def select_player_types() -> Tuple[castle.PlayerType, castle.PlayerType]:
    player1, player2 = None, None
    while True:
        print(f'1) Play a person')
        print(f'2) Play the computer')
        print(f'3) Play the computer against itself')
        choice_str = input(f'Select an option: ')
        try:
            choice = int(choice_str)
            if choice not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print('Invalid option.\n')
            continue

        if choice == 1:
            player1 = castle.PlayerType.HUMAN
            player2 = castle.PlayerType.HUMAN
        elif choice == 2:
            player1 = castle.PlayerType.HUMAN
            player2 = castle.PlayerType.COMPUTER
        elif choice == 3:
            player1 = castle.PlayerType.COMPUTER
            player2 = castle.PlayerType.COMPUTER
        break
    return player1, player2


def play_constructed_game(g: castle.Game):
    g.board.pretty_print()
    while not g.finished:
        print(f'white short {g.can_castle(castle.Color.WHITE, True)}')
        print(f'white long {g.can_castle(castle.Color.WHITE, False)}')
        print(f'black short {g.can_castle(castle.Color.BLACK, True)}')
        print(f'black long {g.can_castle(castle.Color.BLACK, False)}')
        g.play_turn()

    winning_prefix = f'Game over by '
    if g.winner == castle.Winner.DRAW:
        winning_prefix += 'stalemate'
    else:
        winning_prefix += 'checkmate'
    winning_text = f'{winning_prefix}. Winner: {g.winner.name.title()}'
    print(winning_text)


def play_game():
    player1, player2 = select_player_types()
    g = castle.Game(player1, player2)
    play_constructed_game(g)


def test_perft():
    g = castle.Game(castle.PlayerType.HUMAN, castle.PlayerType.HUMAN)
    g.board.pretty_print()
    for i in range(10):
        print(f'perft({i}) = {g.perft(i)}')


def test_perft2():
    g = castle.Game(castle.PlayerType.HUMAN, castle.PlayerType.HUMAN)
    g.board.clear()
    # https://sites.google.com/site/numptychess/perft/position-3
    g.board.place_piece(castle.Piece(castle.PieceType.ROOK, castle.Color.BLACK), 'a8')
    g.board.place_piece(castle.Piece(castle.PieceType.KING, castle.Color.BLACK), 'e8')
    g.board.place_piece(castle.Piece(castle.PieceType.ROOK, castle.Color.BLACK), 'h8')
    g.board.place_piece(castle.Piece(castle.PieceType.PAWN, castle.Color.BLACK), 'a7')
    g.board.place_piece(castle.Piece(castle.PieceType.PAWN, castle.Color.BLACK), 'h7')
    g.board.place_piece(castle.Piece(castle.PieceType.BISHOP, castle.Color.WHITE), 'a5')
    g.board.place_piece(castle.Piece(castle.PieceType.PAWN, castle.Color.BLACK), 'b4')
    g.board.place_piece(castle.Piece(castle.PieceType.PAWN, castle.Color.BLACK), 'c4')
    g.board.place_piece(castle.Piece(castle.PieceType.PAWN, castle.Color.BLACK), 'e4')
    g.board.place_piece(castle.Piece(castle.PieceType.BISHOP, castle.Color.BLACK), 'd3')
    g.board.place_piece(castle.Piece(castle.PieceType.PAWN, castle.Color.WHITE), 'a2')
    g.board.place_piece(castle.Piece(castle.PieceType.PAWN, castle.Color.WHITE), 'h2')
    g.board.place_piece(castle.Piece(castle.PieceType.ROOK, castle.Color.WHITE), 'a1')
    g.board.place_piece(castle.Piece(castle.PieceType.KING, castle.Color.WHITE), 'e1')
    g.board.place_piece(castle.Piece(castle.PieceType.ROOK, castle.Color.WHITE), 'h1')
    g.board.pretty_print()
    for i in range(2):
        print(f'perft({i}) = {g.perft(i)}')


def fen():
    # f = castle.FenGameConstructor('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    game = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
    game = 'r3k2r/p6p/8/B7/1pp1p3/3b4/P6P/R3K2R w KQkq - 0 1'
    game = '8/5p2/8/2k3P1/p3K3/8/1P6/8 b - - 0 1'
    f = castle.FenGameConstructor(game)
    return f.game


def main():
    print(f'Welcome to castle, a litte chess engine.\n')
    # test_perft()
    g = fen()
    print('returned')
    g.print_perft(5)
    play_constructed_game(g)
    # play_game()


if __name__ == '__main__':
    main()
