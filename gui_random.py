import sys
import pygame
from random import randrange

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
    # Draw white background
    screen.fill(white)
    # Draw the board
    for j in range(8):
        for i in range(4):
            # Every other row should be offset
            if j % 2 == 0:
                offset = int(width / 8)
            else:
                offset = 0

            pygame.draw.rect(
                screen, grey, (offset + 200 * i, 100 * j,
                               width / 8, height / 8), 0
            )


def draw_pieces(board, screen):
    # crown_img = pygame.image.load("Assets/crown.png")
    # pygame.transform.scale(crown_img, (25, 25))
    for row in board:
        for item in row:
            if item != 0:
                if item.white:
                    color = white
                else:
                    color = black

                radius = 35

                x_center, y_center = 50 + 100 * item.x, 50 + 100 * item.y
                pygame.draw.circle(
                    screen, color, (x_center, y_center), radius
                )
                # Draw circle outline
                pygame.draw.circle(
                    screen, red, (x_center, y_center), radius, 2
                )

                # if item.crowned:
                #     screen.blit(crown_img, (x_center, y_center))


def main():
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Checkers")
    font = pygame.font.SysFont("Times New Roman", 45)

    # A 2d array to store the pieces
    board = [[0 for _ in range(8)] for _ in range(8)]
    # Populate the board with piece objects - 0 indicates an empty field
    setup_board(board)

    # Game loop
    game_over = False
    white_turn = True

    # Game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        draw_board(screen)
        draw_pieces(board, screen)
        # pygame.time.delay(100)
        pygame.display.update()

        capturing_piece = None
        turn_ongoing = True
        while turn_ongoing:
            if white_turn:
                print("White to play")
            else:
                print("Black to play")

            # Get moves given game state and turn
            moves = get_moves(board, white_turn, capturing_piece)

            # Get random moves
            selected_piece = randrange(len(moves))
            selected_move = randrange(len(moves[selected_piece][2]))

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
                    # If it cannot make any more captures end the turn
                    if not can_capture:
                        turn_ongoing = False
                # If no subsequent captures can be made with the piece end the players turn
                else:
                    turn_ongoing = False
            else:
                turn_ongoing = False
        white_turn = not white_turn

        pygame.time.delay(150)

    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    main()
