# vq22301_EMATM0048

## Part 1 - Dots & Boxes (Squares) Game

This repository contains files relating to the Dots & Boxes (referred to as squares) game, a 19th century game created by French mathematician Edouard Lucas. The game takes the player through several menus, allowing them to choose board size (MxN, where 3 < M,N < 10), game mode (2 player, 1 player (random computer) or 1 player (smart(er) computer), and game type in the case of 1 player (smart(er) computer) (turn-based or simultaneous). The game then commences, responding to user input choices and, in the case of 1 player games, program-generated computer moves. Points are awarded for completed squares and the player with the most points at the end of the game wins. Choose to play again or end game. Instructions for the game are displayed upon running main.py.

The game consists of three programs, main.py, board.py and player.py. The board.py module contains the "Board" class, which initialises the attributes and methods relating to the game board. The player.py module contains multiple classes, which, taking advantage of inheritance and polymorphism, govern the attributes and methods required for different types of players, e.g. human players vs computer players. Main.py dictates the flow of the game, including collecting and responding to user input and calling methods from the classes imported from board.py and player.py.

Below are some design decisions to note:

 - In terms of design, to reduce repetition and maximise code elegance, the player object was passed to board methods and for loops were used to get relevant attributes, e.g. board markings, for each player. 
 - Where user input is required, error handling is used to catch errors and prompt the user to enter a valid input, preventing game interruption. `except Exception` is used, however, to allow KeyboardInterrupt.
 - The smart computer player will choose the line that will complete the most squares (prioritising moves that will complete 2 squares over 1 square, and 1 square over none).
 - In simultaneous mode, when the computer and human player select the same square, if the move completes a square, the square is marked with "DR" (shorthand for "draw") and lines are marked with either "--" or "  !  ". This helps distinguish completed squares and different line types.
 - In simultaneous mode, when there are two lines remaining and neither complete a square (a.k.a. when the last two lines to be drawn are for a corner square), both the computer and human players may select the same line. This avoids a situation where the player cannot finish the game.

## Part 2 - Data Analytics

The following additional libraries were used in the analysis. Below is a description of how each was used:

 1) Pandas - open source data analysis and manipulation tool, built on top of the Python programming language (https://pandas.pydata.org/).
 2) Numpy - package for scientific computing with Python (https://numpy.org/)
 3) Matplotlib - library for creating static, animated, and interactive visualizations in Python (https://matplotlib.org/).
 4) yfinance - yfinance offers a threaded and Pythonic way to download market data from Yahoo! finance (https://pypi.org/project/yfinance/).
 5) seaborn - a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics (https://seaborn.pydata.org/).
 6) statsmodels.tsa.stattools.adfuller() - Function to run the Augmented Dickey-Fuller test. Used to test for data stationarity (https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html).
 7) statsmodels.tsa.seasonal.seasonal_decompose() - method to assess seasonal decomposition using moving averages. Used to visualise trend and seasonality (https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html).
 8) pmdarima.arima.auto_arima() - an ARIMA estimator used to find the optimal order parameters for our arima models (https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.ARIMA.html).
 9) statsmodels.tsa.arima.model.ARIMA() - method to run ARIMA models on the data (https://www.statsmodels.org/dev/generated/statsmodels.tsa.arima.model.ARIMA.html).
 10) sklearn.metrics.mean_squared_error() - method to find the mean squared error of a model (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html).

libraries included in site-packages repo: pmdarima, statsmodels, yfinance. It is assumed that the assessor already has the other packages listed above installed.

Github repository link: https://github.com/mwynne-bristol/vq22301_EMATM0048
