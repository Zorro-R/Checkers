import numpy as np
import copy
from main import get_moves, display_board
from piece import Piece


def static_evaluation(board):
    evaluation = 0
    # Count up the white pieces and subtract the black pieces
    for row in board:
        for item in row:
            if item != 0:
                if item.white:
                    evaluation += 1
                else:
                    evaluation -= 1


# def minimax(board, white_turn, depth):

#     # Base case - depth is 0
#     if depth == 0:
#         return static_evaluation(board)


# board for testing double capture scenarios
test_board1 = [[0 for _ in range(8)] for _ in range(8)]
test_board1[0][7] = Piece((7, 0), False)
test_board1[1][2] = Piece((2, 1), False)
test_board1[1][6] = Piece((6, 1), False)
test_board1[2][1] = Piece((1, 2))
test_board1[2][5] = Piece((5, 2))
test_board1[4][5] = Piece((5, 4))
test_board1[2][3] = Piece((3, 2))
test_board1[4][3] = Piece((3, 4))
test_board1[6][3] = Piece((3, 6))

display_board(test_board1)


def piece_recursive_moves(board, piece):
    moves = piece.potential_moves(board)
    print(moves)
    # Base case - piece can make no moves or only non-capturing moves
    if moves == None:
        return []
    # Else if only non-capturing moves can be made return these
    elif moves[0] == False:
        return moves
    # Otherwise simulate capturing move for each possible capture
    for move in moves[1]:
        print(move)
        x, y = piece.x, piece.y
        new_x, new_y = move
        # Simulate the move on a copy of the board
        board_copy = copy.deepcopy(board)
        board_copy[new_y][new_x] = piece
        # Update the pieces position
        piece.update((new_x, new_y))
        # Remove captured piece
        dx, dy = new_x - x, new_y - y
        captured_x, captured_y = x + int(dx / 2), y + int(dy / 2)
        board[captured_y][captured_x] = 0

        # Recurse
        return [moves[0], moves[1] + piece_recursive_moves(board, piece)]


piece = test_board1[1][2]
piece_recursive_moves(test_board1, piece)
