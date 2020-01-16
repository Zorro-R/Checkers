import sys
import pygame
from random import randrange
from numpy import floor

from main import setup_board, get_moves
import piece

# Constants
size = width, height = 800, 800
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
grey = 200, 200, 200


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
                if item.white:
                    color = white
                else:
                    color = black

                radius = 35

                x_center, y_center = 50 + 100 * item.x, 50 + 100 * item.y
                # Draw filled circle
                pygame.draw.circle(
                    screen, color, (x_center, y_center), radius
                )

                if item.crowned:
                    if item.white:
                        crown_color = black
                    else:
                        crown_color = white

                    pygame.draw.circle(
                        screen, crown_color, (x_center, y_center), int(
                            radius / 2)
                    )

                # Draw circle outline in red if not selected else green
                if item.selected:
                    outline_color = green
                else:
                    outline_color = red

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


def select_piece(board, moves):
    # Get user input
    selected_piece = None

    while selected_piece == None:
        # Check system events
        for event in pygame.event.get():
            # Quit if desired
            if event.type == pygame.QUIT:
                game_over = True
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

    # Game loop
    game_over = False
    white_turn = True
    while not game_over:
        # Check for call to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.display.quit()
                pygame.quit()
                sys.exit(0)

        capturing_piece = None
        turn_ongoing = True
        while turn_ongoing:
            # Get moves given game state and turn
            moves = get_moves(board, white_turn, capturing_piece)

            # Get user input
            selected_piece = select_piece(board, moves)

            selected_move = None
            while selected_move == None:
                # Check system events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit(0)

                    # If mouse is clicked
                    if event.type == pygame.MOUSEBUTTONUP:
                        selected_pos = pos_to_coors(pygame.mouse.get_pos())
                        # If selection is valid
                        if selected_pos in [move for move in moves[selected_piece][2]]:
                            selected_move = [
                                move for move in moves[selected_piece][2]].index(selected_pos)

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

            # If piece made a capture check if any new captures must be made
            if capturing_move:
                # Remove the captured piece from the board
                dx, dy = new_x - x, new_y - y
                captured_x, captured_y = x + int(dx / 2), y + int(dy / 2)
                board[captured_y][captured_x] = 0

                # Set it as the capturing_piece to be used as an argument for the potential_moves() function.
                capturing_piece = piece

                # If piece can still move
                if piece.potential_moves(board) != None:
                    can_capture, _ = piece.potential_moves(board)
                    # If it cannot make any more captures unselect it and end the turn
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

        white_turn = not white_turn

        # Check if the game is over
        white_exists = False
        black_exists = False
        for row in board:
            for item in row:
                if item != 0:
                    if item.white:
                        white_exists = True
                    else:
                        black_exists = True

        if not white_exists or not black_exists:
            game_over = True

    pygame.display.quit()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    main()
