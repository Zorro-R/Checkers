import sys
import pygame
from random import randrange
from numpy import floor

# Custom classes
from piece import Piece

# Constants
size = width, height = 800, 800
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
grey = 200, 200, 200


def setup_board(board):
    '''
    Setup the board by populating it with Piece objects
    Args:
    board -> List[List[Piece, Int]]
    Returns:
    None
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


def draw_board(screen):
    """
    Draws a basic checker board pattern on a screen object.
    Args:
    screen -> pygame.Surface
    Returns:
    None
    """
    # Draw white background
    screen.fill(white)
    # Overlay black squares onto the background
    for i in range(4):
        for j in range(8):
            # Every other row should be offset by one square
            if j % 2 == 0:
                offset = int(width / 8)
            else:
                offset = 0
            # Draw black square in given position
            pygame.draw.rect(
                screen, grey, (offset + 200 * i, 100 * j,
                               int(width / 8), int(height / 8)), 0
            )


def draw_pieces(board, screen):
    """
    Takes a board object and draws all pieces on a
    screen object with appropriate colors, positioning,
    and crowned status.
    Args:
    board -> List[List[Piece, Int]]
    screen -> pygame.Surface
    Returns:
    None
    """
    for row in board:
        for item in row:
            if item != 0:
                # Select color
                color = white if item.white else black

                radius = 35

                x_center, y_center = 50 + 100 * item.x, 50 + 100 * item.y
                # Draw filled circle
                pygame.draw.circle(
                    screen, color, (x_center, y_center), radius
                )

                # If piece is crowned fill it with a smaller circle of opposite color
                if item.crowned:
                    crown_color = black if item.white else white

                    pygame.draw.circle(
                        screen, crown_color, (x_center, y_center), int(
                            radius / 2)
                    )

                # Draw circle outline in red if not selected else green
                outline_color = green if item.selected else red

                pygame.draw.circle(
                    screen, outline_color, (x_center, y_center), radius, 2
                )


def pos_to_coors(pos):
    """
    Takes a pos tuple containing x and y position on the screen
    from the top left and returns a tuple indicating the coordinates
    of that square. Useful for converting from a mouse position.
    Args:
    pos -> Tuple(x, y)
    Returns:
    Tuple(x, y)
    """
    x, y = pos
    # Convert coordinates to a position on the board
    x_coord, y_coord = int(floor(x/100)), int(floor(y/100))

    return (x_coord, y_coord)


def get_moves(board, white_turn, capturing_piece=None):
    """
    Takes a board object and a boolean representing which players turn it is
    and returns a list of tuples representing what legal moves can be made
    given the gamestate. It can be fed a capturing_piece object in order to 
    return only the moves of that piece.
    Args:
    board -> List[Piece, Int]
    white_turn -> Bool
    capturing_piece -> Piece, None
    Returns:
    legal_moves -> List[Tuple(Tuple, Bool, List[Tuple])]
    """

    # If no capturing move was made
    if capturing_piece == None:
        # Get all pieces and flatten to a 1d list
        all_pieces = [piece for row in [[item for item in row if isinstance(
            item, Piece)] for row in board] for piece in row]

        if white_turn:
            # Get white pieces
            pieces = [piece for piece in all_pieces if piece.white]
        else:
            # Get black pieces
            pieces = [piece for piece in all_pieces if not piece.white]

    else:
        pieces = [capturing_piece]

    move_info = []
    # Check for possible moves for pieces of a given color
    for piece in pieces:
        moves = piece.potential_moves(board)
        # If the piece can move add its position and a list of its moves to move_info
        if moves != None:
            move_info.append(((piece.x, piece.y), moves))

    # Only count capturing moves as legal moves if such capturing moves exist.
    capturing_moves = [(info[0], info[1][0], info[1][1])
                       for info in move_info if info[1][0] == True]
    if len(capturing_moves) > 0:
        legal_moves = capturing_moves
    else:
        legal_moves = [(info[0], info[1][0], info[1][1])
                       for info in move_info if info[1][0] == False]

    return legal_moves


def select_piece(board, moves):

    selected_piece = None

    while selected_piece == None:
        # Check system events
        for event in pygame.event.get():
            # Quit if desired
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # If mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                selected_pos = pos_to_coors(pygame.mouse.get_pos())

                # Check if user selected a valid piece
                if selected_pos in [move[0] for move in moves]:
                    # Get index of the piece in moves list
                    selected_piece = [move[0]
                                      for move in moves].index(selected_pos)
                    # Select the piece
                    x_selected, y_selected = selected_pos
                    board[y_selected][x_selected].selected = True

    # Once a piece has been selected, return its position in the moves array
    return selected_piece


def select_move(board, moves, selected_piece):
    selected_move = None
    while selected_move == None:
        # Check system events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # If mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                selected_pos = pos_to_coors(pygame.mouse.get_pos())
                # If selection is valid
                if selected_pos in [move for move in moves[selected_piece][2]]:
                    selected_move = [
                        move for move in moves[selected_piece][2]].index(selected_pos)

    # Once player has selected a valid move return the index
    # of that move in the list of moves
    return selected_move


def is_game_over(board):
    """
    Function that takes a board object and checks if the game is
    over or tied and returns a tuple containing information on
    the winner and whether or not the game is over or has been
    tied.
    Args:
    board -> List[List[Piece, Int]]
    Returns:
    Tuple(Bool)
    """
    # Assume default gamestate values
    game_over, game_tied, white_wins = False, False, None

    # Get white and black moves
    white_moves = get_moves(board, True)
    black_moves = get_moves(board, False)

    # Check if game is tied, i.e if neither player can make any valid moves
    if white_moves == [] and black_moves == []:
        game_tied = True
        game_over = True
    # Otherwise check if either player won because their opponent cannot move
    else:
        # See if white and black have valid moves
        can_white_move = True if white_moves != [] else False
        can_black_move = True if black_moves != [] else False

        if can_white_move and not can_black_move:
            white_wins = True
            game_over = True
        elif can_black_move and not can_white_move:
            white_wins = False
            game_over = True

    # Return updated gamestate values
    return (game_over, game_tied, white_wins)


def main():
    """
    Main function to control the game loop for getting player 
    input, executing moves and displaying the current gamestate.
    """
    # Setup the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Checkers")

    # A 2d array to store the pieces
    board = [[0 for _ in range(8)] for _ in range(8)]
    # Populate the board with piece objects - 0 indicates an empty field
    setup_board(board)

    # Display the board
    draw_board(screen)
    draw_pieces(board, screen)
    pygame.display.update()

    # Gamestate variables
    white_turn = True
    game_over = False
    white_wins = None
    game_tied = False

    # Print an appropriate message if the game is over
    print("Game Tied") if game_tied else None
    if game_over and not game_tied and white_wins != None:
        print("White won!") if white_wins else print("Black won!")

    # Game loop
    while not game_over:
        # Check for call to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit(0)

        # Print who's turn it is
        print("White to play") if white_turn else print("Black to play")

        capturing_piece = None
        turn_ongoing = True
        while turn_ongoing and not game_over and not game_tied:
            # Get moves given game state and turn
            moves = get_moves(board, white_turn, capturing_piece)
            # Check

            # Get user input
            selected_piece = select_piece(board, moves)
            selected_move = select_move(board, moves, selected_piece)

            # Get info about the desired move
            x, y = moves[selected_piece][0]
            new_x, new_y = moves[selected_piece][2][selected_move]
            # Bool representing whether a capturing move can be made
            capturing_move = moves[selected_piece][1]

            # Move the piece accordingly
            piece = board[y][x]
            board[new_y][new_x] = piece
            board[y][x] = 0
            # Update the position, check for promotion to king
            piece.update((new_x, new_y))

            # If piece made a capture check if any new captures must be made
            if capturing_move:
                # Set it as the capturing_piece to be used as an argument
                # for the potential_moves() function.
                capturing_piece = piece

                # Remove the captured piece from the board
                dx, dy = new_x - x, new_y - y
                captured_x, captured_y = x + int(dx / 2), y + int(dy / 2)
                board[captured_y][captured_x] = 0

                # If piece that captured can still move
                if capturing_piece.potential_moves(board) != None:
                    can_capture, _ = piece.potential_moves(board)
                    # If it cannot make any more captures end the turn
                    if not can_capture:
                        # Unselect the piece
                        board[new_y][new_x].selected = False
                        # End turn
                        turn_ongoing = False

                # If no subsequent captures can be made with the piece end the players turn
                else:
                    # Unselect the piece
                    board[new_y][new_x].selected = False
                    # End turn
                    turn_ongoing = False
            else:
                 # Unselect the piece
                board[new_y][new_x].selected = False
                # End turn
                turn_ongoing = False

            # Display updated position
            draw_board(screen)
            draw_pieces(board, screen)
            pygame.display.update()

        # Change who's turn it is
        white_turn = not white_turn

        # Check if the game is over or tied
        game_over, game_tied, white_wins = is_game_over(board)


if __name__ == "__main__":
    pygame.init()
    main()
