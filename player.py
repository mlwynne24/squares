"""Morgan Wynne, Student Number 2259639

This program contains classes to represent players. Each player class 
inherits from another, with the "Player" class acting as the parent at 
the top of the class hierarchy.
"""

import random


class Player:
    """Stores methods and attributes for the Player class, which has 
    the following functionality:

    1) Stores the player name, number, score, type (human or computer), 
    and grid coordinates and complete squares (for simultaneous mode).
    2) Converts player input or computer moves to a set of coordinates 
    on the grid attribute of the Board object. 
    """

    def __init__(self, board, name, player_number, score=0):
        """Initialises the Player object.
        
        Takes the board object, player name, player number, and 
        starting score (default=0) as parameters.
        """
        self.board = board
        self.name = name
        self.player_number = player_number
        self.score = score
        self.type = "human"
        self.grid_coordinates = None
        self.squares_complete = None

    def move(self, move):
        """Converts parameter "move", a string object in the form of two 
        coordinates (e.g. "(1,2)(2,2)") to a single coordinate to be 
        marked as a line on the grid attribute of the Board object.

        Returns coordinates as a tuple (x,y).
        """
        x1, x2 = float(move[1]), float(move[6])
        y1, y2 = float(move[3]), float(move[8])
        assert (((x1 == x2 and (y1 == y2 - 1 or y1 == y2 + 1)) or 
            (y1 == y2 and (x1 == x2 - 1 or x1 == x2 + 1))) and 
            (0 < x1 < 10 and 0 < x2 < 10 and 0 < y1 < 10 and 0 < y2 < 10) and 
            (len(move) == 10))
        if any([
            move[0] != "(", move[5] != "(", move[4] != ")", 
            move[9] != ")", move[2] != ",", move[7] != ","
        ]):
            raise ValueError
        if x1 == x2:  # If the line is horizontal
            y = int(y1 + y2 - 2)
            x = int((x1 - 1) * 2)
        if y1 == y2:  # If the line is vertical
            x = int(x1 + x2 - 2)
            y = int((y1-1) * 2)
        return (x, y)


class Player1(Player):
    """Stores methods and attributes for the Player 1 class, which 
    inherits methods and attributes from the Player class.

    Attributes, markings and square_marking, are added to distinguish 
    Player 1 moves from Player 2 moves on the grid attribute of the 
    Board object. 
    """

    def __init__(self, board, score=0, player_number=1, name="Player 1"):
        """Initialises the Player 1 object."""

        super().__init__(board, name, player_number, score)
        self.markings = ["__", "  |  "]
        self.square_marking = "P1"


class Player2(Player):
    """Stores methods and attributes for the Player 2 class, which 
    inherits methods and attributes from the Player class.

    Attributes, markings and square_marking, are added for the same 
    reasons as above.
    """

    def __init__(self, board, score=0, player_number=2, name="Player 2"):
        """Initialises the Player 2 object."""

        super().__init__(board, name, player_number, score)
        self.markings = ["..", "  :  "]
        self.square_marking = "P2"


class Dumb_Computer(Player2):
    """Stores methods and attributes for the Dumb_Computer class, which 
    inherits methods and attributes from the Player2 class. Players 
    of this type make moves randomly.

    The attribute, type, is changed and two new methods are added from 
    Player 2 class to allow objects to generate random, valid moves.
    """

    def __init__(self, board, score=0, player_number=2, name="Player 2"):

        super().__init__(board, score, player_number, name)
        self.type = "computer"

    def get_random_move(self):
        """Returns random, valid move.
        
        Calls the get_empty_spaces() method from the board object to 
        get a list of all empty coordinates. A random coordinate is 
        then selected. The convert_cpu_human() method is returned 
        with the x and y values for the random coordinate as parameters.
        """
        possible_moves = self.board.get_empty_spaces()
        move = possible_moves[random.randint(0, len(possible_moves) - 1)]
        x, y = move[0], move[1]
        return self.convert_cpu_human(x, y)

    def convert_cpu_human(self, x, y):
        """Converts computer random move generation output to the same 
        format as human player input.

        This can then be used as a parameter to the Player.move() function 
        and displayed to the user.
        """
        if x % 2 == 0:  # If horizontal line
            return f'({int((x/2)+1)},{int(((y-1)/2)+1)})({int((x/2)+1)},{int(((y+1)/2)+1)})'
        else:  # If vertical line
            return f'({int(((x-1)/2)+1)},{int((y/2)+1)})({int(((x+1)/2)+1)},{int((y/2)+1)})'


class Smart_Computer(Dumb_Computer):
    """Stores methods and attributes for the Smart_Computer class, which 
    inherits methods and attributes from the Dumb_Computer class. Players 
    of this type make moves more smartly.

    The new method, get_best_move() is added to allow objects to generate 
    moves which complete the most squares on the Board object's grid 
    attribute.
    """

    def __init__(self, board, score=0, player_number=2, name="Player 2"):

        super().__init__(board, score, player_number, name)

    def get_best_move(self):
        """Gets all available, empty spaces in the grid and checks if 
        any will complete 1 or 2 squares.
        
        If there are lines that will complete 2 squares, a random option 
        from these will be chosen. If not, a random line will be selected 
        from those that complete 1 square. If there are no lines that 
        will complete a square, get_random_move() is called. 
        
        The convert_cpu_human() method is returned with the x and y 
        values for the move coordinates as parameters.
        """
        good_moves = {1: [], 2: []}
        possible_moves = self.board.get_empty_spaces()
        for move in possible_moves:
            completed_squares = self.board.check_complete_square(
                move[0], move[1])[0]
            if completed_squares >= 1:
                good_moves[completed_squares].append(move)

        if good_moves[2]:
            move = good_moves[2][random.randint(0, len(good_moves[2]) - 1)]
            x, y = move[0], move[1]
        elif good_moves[1]:
            move = good_moves[1][random.randint(0, len(good_moves[1]) - 1)]
            x, y = move[0], move[1]
        else:
            return self.get_random_move()
        return self.convert_cpu_human(x, y)