import numpy as np
from main import get_moves


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


def minimax(board, white_turn, depth):

    # Base case - depth is 0
    if depth == 0:
        return static_evaluation(board)

    # Get possible moves
    else:
        if white_turn:
            moves = get_moves(board, white_turn, capturing_piece)
            for move in moves:
                # Simulate move to get new board position
                # Then evaluate new board position
                # Return move leading to max gain
                #[minimax(board, white_turn, depth)]
            # max(minimax(board))

#def simulate_move(board, moves, white_turn, selected_piece, simulate_move):
    

# def recursive_moves(board, white_turn, turn_ongoing=True):
#     """
#     Given a game state and a players turn, return a list
#     of moves where all sequential moves are counted as a
#     single move. By default turn_ongoing is true.
#     Args:
#     board -> List[Piece, Int]
#     white_turn -> Bool
#     turn_ongoing -> Bool
#     """
#     # Base case - end of turn
#     if turn_ongoing == False:
#         # Get moves given gamestate and turn
#         moves = get_moves(board, white_turn, None)

#     # Sequential moves must be made
#     else:
        
#         # Get moves given gamestate and turn
#         moves = get_moves(board, white_turn, capturing_piece)

#         # Get info about the desired move
#         x, y = moves[selected_piece][0]
#         new_x, new_y = moves[selected_piece][2][selected_move]
#         capturing_move = moves[selected_piece][1]
#         # Move the piece accordingly
#         piece = board[y][x]
#         board[new_y][new_x] = piece
#         board[y][x] = 0
#         # Update the position, check for promotion to king
#         piece.update((new_x, new_y))
#         # If piece made a capture check if any new captures must be made
#         if capturing_move:
#             # Remove the captured piece from the board
#             dx, dy = new_x - x, new_y - y
#             captured_x, captured_y = x + int(dx / 2), y + int(dy / 2)
#             board[captured_y][captured_x] = 0

#             # Set it as the capturing_piece to be used as an argument for the potential_moves() function.
#             capturing_piece = piece
            
#             # If piece can still move
#             if piece.potential_moves(board) != None:
#                 can_capture, _ = piece.potential_moves(board)
#                 # If it cannot make any more captures end the turn
#                 if not can_capture:
#                     turn_ongoing = False
#             # If no subsequent captures can be made with the piece end the players turn
#             else:
#                 turn_ongoing = False
#         else:
#             turn_ongoing = False

def recursive_moves(board, white_turn):
    """
    Returns:
    moves -> List[Tuple(Tuple, Bool, List[Tuple])]
    """
    pieces = []

    for row in board:
        for item in row:
            if item != 0:
                # If item is a piece
                if item.white and white_turn:
                    pieces.append(item)
                elif not item.white and not white_turn:
                    pieces.append(item)
    
    # Find all possible moves of any piece
    for piece in pieces:
        # Get info about the desired move
        x, y = moves[selected_piece][0]
        new_x, new_y = moves[selected_piece][2][selected_move]
        capturing_move = moves[selected_piece][1]
        # Move the piece accordingly
        piece = board[y][x]
        board[new_y][new_x] = piece
        board[y][x] = 0
        # Update the position, check for promotion to king
        piece.update((new_x, new_y))


def piece_recursive_moves(board, piece):
    moves = piece.potential_moves(board)

    # Base case - piece can make no moves or only non-capturing moves
    if moves == None:
        return []
    # Else if only non-capturing moves can be made return these
    elif moves[0] == False:
        return piece.potential_moves(board)
    # Otherwise simulate capturing move for each possible capture
    for move in moves:
        


        return piece_recursive_moves(board, piece)
        
    
    if moves != None:
        # If no capturing moves can be made

# potential_moves()
# Returns:
# Tuple(Bool, List[Tuple(x,y)]) if any moves can be made
# else None