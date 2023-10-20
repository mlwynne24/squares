"""Morgan Wynne, Student Number 2259639

This program holds the main.py script, which is used for running the game.

It takes user input, governs the path the player takes, 
and calls relevant functions from board.py and player.py.
"""

from random import shuffle
from board import Board
from player import *

play_again = True
while (play_again == True):  # Main game menu

    while (True):  # Board size menu
        try:
            board_size = str(input(
                "\nWelcome to Squares!\n\nINSTRUCTIONS\n\nPlayers alternate drawing a horizontal or a vertical line between adjacent dots. A player that completes the fourth side of a square wins that square and must play again. The player with the most points once all of the squares have been completed wins.\n\nWhat size board would you like to play on?\n\n(input as mxn where m,n<10 where m,n>3. For example: 8x5 or 4x7): ")).lower()
            squares_board = Board(board_size)
            break
        except AssertionError as e:
            print(e)
        except Exception:
            print(
                "\nPlease enter a valid value for board size. For example: 8x5 or 4x7")

    while (True):  # Game mode menu
        try:
            game_mode = int(input(
                "\n\nPlease enter a number (1, 2 or 3) for how you would like to play!\n\n1) 2 Player\n2) 1 Player (vs. computer that randomly selects moves)\n3) 1 Player (vs. SMART(er) Computer. Choose to play in TURN-BASED or SIMULTANEOUS mode)\n\nGame mode: "))
            assert game_mode in [1, 2, 3]
            break
        except Exception:
            print("\nInvalid entry. Please type one of 1, 2, or 3")

    player_1 = Player1(squares_board)
    if game_mode == 1:
        player_2 = Player2(squares_board)
        game_type = 1
    elif game_mode == 2:
        player_2 = Dumb_Computer(squares_board)
        game_type = 1
    else:
        player_2 = Smart_Computer(squares_board)

    if player_2.__class__.__name__ == "Smart_Computer":  # Game type (turn-based or simultaneous) menu
        while (True):
            try:
                game_type = int(input(
                    "\n\nWould you like to play in turn-based or simultaneous mode? Please enter a number (1 or 2).\n\n1) Turn-based\n2) Simultaneous (the Computer and Human players play at the same time. If both choose to draw the same side of the box and the side is completing a box, the score is split between players. If the side is not completing a box, they must both choose a different line to draw).\n\nGame mode: "))
                assert game_type in [
                    1, 2], "\nInvalid entry. Please type either 1 or 2"
                break
            except Exception as e:
                print(e)

    print("\n\nYou are Player 1!")

    if game_type == 1:
        players = [player_1, player_2]
        shuffle(players)
        print(f'\n{players[0].name} goes first!')
    else:
        turn = 0

    game_finished = False
    while (game_finished == False):  # Game loop
        if game_type == 1:  # Turn-based game
            for player in players:
                if player.type == "computer":
                    if player.__class__.__name__ == "Dumb_Computer":
                        move = player.get_random_move()
                    if player.__class__.__name__ == "Smart_Computer":
                        move = player.get_best_move()
                    print(f'\nThe Computer chose {move}')
                while (True):  # Human player input
                    try:
                        if player.type == "human":
                            squares_board.__str__(player_1, player_2)
                            move = input(
                                f'\n{player.name} - please enter your move in the form of two adjacent coordinates to draw the line between (e.g. "(1,4)(2,4)" or "(2,2)(2,3)"). Please INCLUDE BRACKETS.\n\nYour move: ')
                        grid_coordinates = player.move(move)
                        if squares_board.is_valid_move(*grid_coordinates):
                            break
                        else:
                            print(
                                "\nA player has already moved here! Please choose again...")
                    except AssertionError:
                        print(
                            "\nInvalid entry. Please make sure your chosen co-ordinates are either vertically or horizontally adjacent, and you can see them on the board")
                    except Exception:
                        print(
                            "\nInvalid format. Please enter your move in the form of two coordinates WITH BRACKETS AND COMMAS. For example: (1,2)(2,2)")
                squares_complete = squares_board.check_complete_square(
                    *grid_coordinates)
                squares_board.grid_update(player, *grid_coordinates)
                squares_board.mark_won_squares(player, squares_complete[1])
                if (squares_complete[0] != 0):
                    p1, p2 = players.index(player_1), players.index(player_2)
                    players[p1], players[p2] = players[p2], players[p1]

        if game_type == 2:  # Simultaneous game
            turn += 1
            move_before = 0
            print(f'\nTURN {turn}:')
            squares_board.__str__(player_1, player_2)
            while (True):  # Loop for if human player chooses the same move as the computer
                while (True):  # Human player input
                    try:
                        human_move = input(
                            f'\nPlayer 1 - please enter your move for turn {turn} in the form of two adjacent coordinates to draw the line between (e.g. "(1,4)(2,4)" or "(2,2)(2,3)"). Please INCLUDE BRACKETS.\n\nYour move: ')
                        if human_move == move_before:
                            print(
                                "\nInvalid entry. You cannot enter the same move again! Please enter a different move.")
                        else:
                            player_1.grid_coordinates = player_1.move(
                                human_move)
                            if squares_board.is_valid_move(
                                    *player_1.grid_coordinates):
                                break
                            else:
                                print(
                                    "\nA player has already moved here! Please choose again...")
                    except AssertionError:
                        print(
                            "\nInvalid entry. Please make sure your chosen co-ordinates are either vertically or horizontally adjacent, and you can see them on the board")
                    except Exception:
                        print(
                            "\nInvalid format. Please enter your move in the form of two coordinates WITH BRACKETS AND COMMAS. For example: (1,2)(2,2)")
                computer_move = player_2.get_best_move()
                while (True):
                    if computer_move == move_before:
                        computer_move = player_2.get_best_move()
                    else:
                        break
                print(f'\nThe Computer chose {computer_move}')
                player_2.grid_coordinates = player_2.move(computer_move)
                for player in [player_1, player_2]:
                    player.squares_complete = squares_board.check_complete_square(
                        *player.grid_coordinates)

                if (player_1.grid_coordinates == player_2.grid_coordinates):  # If players chose the same move
                    if player_1.squares_complete[0] == 0:
                        print(
                            "\nYou and the Computer both chose the same line! Please enter a different move...")
                        if len(squares_board.get_empty_spaces()) <= 2:  # Avoids the situation where there are two moves left for the same corner square, both players select the same move, and both do not complete a square, thus preventing the game from ending.
                            pass
                        move_before = human_move
                        pass
                    else:
                        for player in [player_1, player_2]:
                            squares_board.grid_update(
                                player, *player.grid_coordinates, "draw")
                            squares_board.mark_won_squares(
                                player, player.squares_complete[1], "draw")
                            for square in player.squares_complete[1]:
                                player.score += 0.5
                        break
                else:
                    players = [player_1, player_2]
                    shuffle(players)  # Makes it fair when there is a situation where both players choose different lines on the same square and the square is completed.
                    for player in players:
                        player.squares_complete = squares_board.check_complete_square(
                            *player.grid_coordinates)
                        squares_board.grid_update(
                            player, *player.grid_coordinates)
                        squares_board.mark_won_squares(
                            player, player.squares_complete[1])
                    break
        
        if (squares_board.check_game_won()):
            squares_board.print_winner(player_1, player_2)
            game_finished = True
            break

    while (True):  # Play again menu
        try:
            input_play_again = input(
                "\n\nWould you like to play again? Type 'Y' or 'N': ")
            assert input_play_again in [
                "Y", "N", "y", "n", "yes", "no", "YES", "NO"]
            if (input_play_again.upper() == "N" or 
                    input_play_again.upper() == "NO"):
                print("\nThank you for playing squares today!")
                play_again = False
                break
            else:
                break
        except AssertionError:
            print("\nInvalid entry. Please enter either 'y' or 'n'\n")