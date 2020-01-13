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


def get_moves(board, white_turn):
    """
    Takes a board object and a boolean representing which players turn it is
    and returns a list of tuples representing what legal moves can be made 
    given the gamestate.
    Args:
    board -> List[Piece, Int]
    white_turn -> Bool
    Returns:
    legal_moves -> List[Tuple(Tuple, List[Tuple])]
    """

    # Get all pieces and flatten to a 1d list
    all_pieces = [piece for row in [[item for item in row if isinstance(
        item, Piece)] for row in board] for piece in row]

    if white_turn:
        # Get white pieces
        pieces = [piece for piece in all_pieces if piece.isWhite]
    else:
        # Get black pieces
        pieces = [piece for piece in all_pieces if not piece.isWhite]

    move_info = []
    # Check for possible moves for pieces of a given color
    for piece in pieces:
        moves = piece.potential_moves(board)
        # If the piece can move add its position and a list of its moves to move_info
        if len(moves[1]) > 0:
            move_info.append(((piece.x, piece.y), moves))

    # Only count capturing moves as legal moves if such capturing moves exist.
    capturing_moves = [(info[0], info[1][1])
                       for info in move_info if info[1][0] == True]
    if len(capturing_moves) > 0:
        legal_moves = capturing_moves
    else:
        legal_moves = [(info[0], info[1][1])
                       for info in move_info if info[1][0] == False]

    return legal_moves


def main():
    # A 2d array to store the pieces
    board = [[0 for _ in range(8)] for _ in range(8)]
    # Populate the board with piece objects - 0 indicates an empty field
    setup_board(board)
    display_board(board)

    game_over = False
    white_turn = True

    # Game loop
    while not game_over:
        if white_turn:
            print("White to play")
        else:
            print("Black to play")

        # Get moves given game state and turn
        moves = get_moves(board, white_turn)
        print(moves)

        game_over = True


if __name__ == "__main__":
    main()
