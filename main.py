import numpy as np
from piece import Piece

# print(help(Piece))
# isinstance()
# issubclass()
# "dunder" ==> __ __
# return NotImplemented
# @property
# def instanceMethod(self):
#   ...

# @instanceMethod.setter
# def instanceMethod(self, input):
#   "modify input"
#   self.someProperty = "modified input"


def setup_board(board):
    '''
    Setup the board by populating it with Piece objects 
    '''
    for i in range(4):
        # Add black pieces
        board[0][1 + 2*i] = Piece((1 + 2*i, 0), False)
        board[2][1 + 2*i] = Piece((1 + 2*i, 2), False)
        board[1][2*i] = Piece((2*i, 1), False)
        # Add white pieces
        board[5][2*i] = Piece((2*i, 5))
        board[7][2*i] = Piece((2*i, 7))
        board[6][1 + 2*i] = Piece((1 + 2*i, 6))


def display_board(board):
    """
    Takes a board object and displays the current game state 
    in the commandline.
    Args:
    board -> List(Piece, Int)
    Returns:
    None
    """
    for row in board:
        for item in row:
            if item == 0:
                print("| |", end="")
            else:
                if item.isWhite:
                    print("|X|", end="")
                else:
                    print("|O|", end="")
        print()


def main():
    # A 2d array to store the pieces
    board = [[0 for _ in range(8)] for _ in range(8)]
    # Populate the board with piece objects - 0 indicates an empty field
    setup_board(board)
    display_board(board)
    board[4][1] = Piece((1, 4), False)
    # print(board)
    # print(board[5][0])
    # print(board[5][0].legal_moves(board))


"""
# Get all pieces and flatten to a 1d list
pieces = [piece for row in [[item for item in row if isinstance(
    item, Piece)] for row in board] for piece in row]
white_pieces = [piece for piece in pieces if piece.isWhite]
black_pieces = [piece for piece in pieces if not piece.isWhite]
"""

if __name__ == "__main__":
    main()
