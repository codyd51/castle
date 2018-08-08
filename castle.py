import castle


def main():
    # g = castle.Game()
    # g.board.get_moves(g.board.square_from_notation('a1'))
    b = castle.Board()

    white_rook = castle.Piece(castle.PieceType.ROOK, castle.Color.WHITE)
    black_pawn = castle.Piece(castle.PieceType.PAWN, castle.Color.BLACK)
    b.place_piece(white_rook, 'f4')
    b.place_piece(black_pawn, 'f7')
    print(b.get_moves(b.square_from_notation('f4')))



if __name__ == '__main__':
    main()
