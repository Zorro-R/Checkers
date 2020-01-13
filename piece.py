def pos_on_board(pos):
    """
    Args:
    pos -> Tuple(x, y)
    Returns:
    True if pos on board
    else False
    """
    x, y = pos

    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    else:
        return True


class Piece:
    def __init__(self, pos, white=True):
        self.x, self.y = pos
        self.white = white
        self.crowned = False

    def __repr__(self):
        return f"Piece({(self.x, self.y)}, {self.white})"

    def __str__(self):
        if self.white:
            return f"{(self.x, self.y)}, white, crowned: {self.crowned}"
        else:
            return f"{(self.x, self.y)}, black, crowned: {self.crowned}"

    def potential_moves(self, board):
        """
        Takes a board object containing all pieces and returns the potential
        moves that the piece can make given the board configuration but
        ignoring whether other pieces may be forced to make capturing moves.
        First element of the returning tuple indicates whether a capturing
        move can be made or not.

        Args:
        board -> List[Piece]
        Returns:
        Tuple(Bool, List[Tuple(x,y)]) if any moves can be made
        else None
        """

        # A list to store single square moves
        single_square_moves = []
        # A list to store double square (i.e capturing) moves
        double_square_moves = []

        # A list of vectors to add to the pieces current position to move it
        if not self.crowned:
            # Control which way the piece can move when it is not crowned
            if self.white:
                direction = -1
            else:
                direction = 1
            movement = [(-1, direction), (1, direction)]
        else:
            # If the piece is crowned it can move both up and down
            movement = [(-1, 1), (1, 1), (-1, -1), (1, -1)]

        # Check if the squares are free
        for move in movement:
            # Calculate possible single and double square moves
            dx, dy = move
            new_x1, new_y1 = self.x + dx, self.y + dy  # Single square move
            new_x2, new_y2 = self.x + 2*dx, self.y + 2 * \
                dy  # Double square (i.e capturing) move
            # If move is on the board
            if pos_on_board((new_x1, new_y1)):
                # If square is free add it to potential_moves list
                if board[new_y1][new_x1] == 0:
                    single_square_moves.append((new_x1, new_y1))
                # Otherwise check if the square behind the occupied one is on the board
                elif pos_on_board((new_x2, new_y2)):
                    # If so check that it is free and that the piece being jumped over is opposite colored
                    if board[new_y2][new_x2] == 0 and board[new_y1][new_x1].white != self.white:
                        double_square_moves.append((new_x2, new_y2))

        # If there are capturing moves, only return these. Otherwise return single square moves.
        # The True / False in the tuple indicates whether a capturing move can be made or not.
        if len(double_square_moves) > 0:
            return (True, double_square_moves)
        # Return None if the piece cannot make any moves
        elif len(single_square_moves) == 0:
            return None
        else:
            return (False, single_square_moves)

    def update(self, pos):
        """
        Updates the position of a piece and also checks if the piece
        is promoted to a king.
        Args:
        pos -> Tuple(x, y)
        Returns:
        True if Piece was crowned
        else False        
        """
        self.x, self.y = pos
        if self.white and self.y == 0:
            self.crowned = True
            return True
        elif self.y == 7:
            self.crowned = True
            return True
        else:
            return False
