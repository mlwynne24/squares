"""Morgan Wynne, Student Number 2259639

This program holds the Board class.
"""


class Board:
    """Stores attributes and methods for objects of the board class, 
    which has the following functionality:

    1) Displays the board,
    2) checks if a move is valid,
    3) updates the board,
    4) checks and marks complete squares,
    5) checks if the game is won,
    6) prints the winner,
    7) and lets the "computer" player objects know,
     which lines can still be drawn.
    """

    def __init__(self, board_size):
        """Initialises the board object.

        Takes user input for board size of type "str". Main attribute is 
        "self.grid", which acts as the board for the game.

        This is done by extracting the x and y sizes from user input,
        creating a list with sufficient spaces, and filling the grid
        with tuples for dots and sufficient spacing for blank elements
        using two for loops.
        """
        x_pos = board_size.rfind("x")
        self.x = int(board_size[:x_pos])
        self.y = int(board_size[x_pos + 1 :])
        assert x_pos != -1 \
            , '\nInvalid format. Please enter board size in the format "mxn", e.g. 6x4, 7x9'
        assert (3 < self.x <= 9) and (
            3 < self.y <= 9) \
            , '\nInvalid entry. Board size must be bigger than 3x3 and smaller than 10x10'
        self.grid = [["  " for i in range(self.x + (self.x - 1))]  # Creating the board grid as blank spaces
                     for j in range(self.y + (self.y - 1))]
        for row in range(0, self.y*2, 2):  # Adding tuples as the dots
            for col in range(0, self.x*2, 2):
                self.grid[row][col] = (int((row/2)) + 1), int(((col/2) + 1))
        for row in range(1, (self.y*2) - 1, 2):  # Adding in spacing to neaten the board
            for col in range(0, self.x*2, 2):
                self.grid[row][col] = ("     ")

    def __str__(self, player_1, player_2):
        """Prints out the game board to the player.
        
        Takes player objects as parameters to mark their name and score
        at the bottom of the grid. Returns the board image with players
        and scores as a string.
        """
        s = f'\n'
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                s += str(self.grid[i][j])
            s += '\n'
        s += f'\nScores: {player_1.name}: {player_1.score},  {player_2.name}: {player_2.score}'
        return print(s.replace(", ", ","))  # Removes spacing in tuples

    def is_valid_move(self, x, y):
        """Takes the x and y coordinates for a move and checks if that space 
        is still empty. Returns True if the space is empty and false if not.
        """
        if self.grid[x][y] == "  " or self.grid[x][y] == "     ":
            return True
        else:
            return False

    def grid_update(self, player, x, y, status="not draw"):
        """Updates the grid attribute with the player's move.

        Takes the player object who made the move, the coordinates on the 
        board and the "status" - a parameter to describe if the result of the 
        move was a draw or not (relevant to simultaneous game type).

        The grid is marked with the relevant player's markings or different 
        markings if the players selected the same move and the turn was a draw.
        """
        if status == "not draw":
            if x % 2 == 0:
                self.grid[x][y] = player.markings[0]
            else:
                self.grid[x][y] = player.markings[1]
        if status == "draw":
            if x % 2 == 0:
                self.grid[x][y] = "--"
            else:
                self.grid[x][y] = "  !  "

    def check_complete_square(self, x, y):
        """Checks how many squares a move completed and the coordinates 
        of the space to be marked as won as a result.

        Takes the x and y coordinates for the move as parameters and 
        returns a tuple with the number of squares completed at position 
        0 and a list at position 1, which contains coordinates as tuples, 
        which represent the squares to mark as won.
        """
        squares_complete = 0
        squares_to_mark = []
        if x % 2 == 0:  # If line is horizontal
            if x == 0:  # Avoids IndexErrors when the line is in the first row of the grid
                poss_squ_if_horiz = [
                    [self.grid[x + 1][y - 1], self.grid[x + 1][y + 1], 
                    self.grid[x + 2][y]], 
                    "blank spacing"
                    ]
            if x == len(self.grid) - 1:  # Avoids IndexErrors when the line is in the last row of the grid
                poss_squ_if_horiz = [
                    "blank spacing", 
                    [self.grid[x - 1][y - 1], self.grid[x - 1][y + 1], 
                    self.grid[x - 2][y]]
                    ]
            else:  # Possible complete squares are above and below the line when the line is horizontal
                poss_squ_if_horiz = [
                    [self.grid[x + 2][y], self.grid[x + 1][y - 1], 
                    self.grid[x + 1][y + 1]],
                    [self.grid[x - 1][y - 1], self.grid[x - 1][y + 1], 
                    self.grid[x - 2][y]]
                    ]
            for possible_square in poss_squ_if_horiz:
                if all(item in [
                    "..", "__", "  |  ", "  :  ", "--", "  !  "
                ] for item in possible_square):
                    if possible_square == poss_squ_if_horiz[0]:
                        squares_to_mark.append((x + 1, y))
                    if possible_square == poss_squ_if_horiz[1]:
                        squares_to_mark.append((x - 1, y))
                    squares_complete += 1
        else:  # If line is vertical
            if y == 0:  # Avoids IndexErrors when the line is in the first column of the grid
                poss_squ_if_vert = [
                    "blank spacing", 
                    [self.grid[x - 1][y + 1], self.grid[x + 1][y + 1], 
                    self.grid[x][y + 2]]
                    ]
            elif y == len(self.grid[0]) - 1:  # Avoids IndexErrors when the line is in the last column of the grid
                poss_squ_if_vert = [
                    [self.grid[x - 1][y - 1], self.grid[x + 1][y - 1], 
                    self.grid[x][y - 2]], 
                    "blank spacing"
                    ]
            else:  # Possible complete squares are to the left and right of the line when the line is vertical
                poss_squ_if_vert = [
                    [self.grid[x][y - 2], self.grid[x - 1][y - 1], 
                    self.grid[x + 1][y - 1]], 
                    [self.grid[x - 1][y + 1], self.grid[x + 1][y + 1], 
                    self.grid[x][y + 2]]
                    ]
            for possible_square in poss_squ_if_vert:
                if all(item in [
                    "..", "__", "  |  ", "  :  ", "--", "  !  "
                ] for item in possible_square):
                    if possible_square == poss_squ_if_vert[0]:
                        squares_to_mark.append((x, y - 1))
                    if possible_square == poss_squ_if_vert[1]:
                        squares_to_mark.append((x, y + 1))
                    squares_complete += 1
        return (squares_complete, squares_to_mark)

    def mark_won_squares(self, player, squares_to_mark, status="not draw"):
        """Marks won squares with the player's marking, e.g. P1, P2. In the 
        case where a turn is drawn (in simultaneous mode), the square is 
        marked with DR for draw.

        Takes the player who made the move, a list of tuples, representing, 
        coordinates to mark as complete (from the check_complete_square() 
        function), and "status", signifying whether the turn was a draw.
        """
        if status == "not draw":
            for square in squares_to_mark:
                self.grid[square[0]][square[1]] = player.square_marking
                player.score += 1
        if status == "draw":
            for square in squares_to_mark:
                self.grid[square[0]][square[1]] = "DR"

    def check_game_won(self):
        """Checks whether there are any empty spaces, where lines can be 
        drawn, left to be filled.
        
        If there are no empty cells, meaning the game is finished, it 
        returns True. Otherwise, it returns False.
        """
        empty_cells = 0
        for row in range(0, len(self.grid), 2):
            for col in range(1, len(self.grid[0]) - 1, 2):
                if self.grid[row][col] == "  ":
                    empty_cells += 1
        for row in range(1, len(self.grid) - 1, 2):
            for col in range(0, len(self.grid[0]), 2):
                if self.grid[row][col] == "     ":
                    empty_cells += 1
        if empty_cells == 0:
            return True
        else:
            return False

    def print_winner(self, player_1, player_2):
        """Prints the match result.
        
        Takes both player objects as parameters to get player scores.
        """
        self.__str__(player_1, player_2)
        if player_1.score > player_2.score:
            print(
                f'\nPlayer 1 won with a score of {player_1.score}. Player 2 finished on {player_2.score} points...')
        elif player_2.score > player_1.score:
            print(
                f'\nPlayer 2 won with a score of {player_2.score}. Player 1 finished on {player_1.score} points...')
        else:
            print(
                f'\nThe match was a draw! Player 1 finished on {player_1.score} points and player 2 finished on {player_2.score} points...')

    def get_empty_spaces(self):
        """Returns a list of tuples, which represent coordinates of 
        empty spaces, which can still be filled with player lines.
        """
        empty_spaces = []
        for i in range(0, len(self.grid), 2):
            for j in range(1, len(self.grid[0]) - 1, 2):
                if self.grid[i][j] == "  ":
                    empty_spaces.append((i, j))
        for i in range(1, len(self.grid) - 1, 2):
            for j in range(0, len(self.grid[0]), 2):
                if self.grid[i][j] == "     ":
                    empty_spaces.append((i, j))
        return empty_spaces