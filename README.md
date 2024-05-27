# Sudoku

This is a simple game of Sudoku written in Python that uses the backtracking algorithm.

The primary solver module works as follows:
* A random 9-by-9 unsolved Sudoku puzzle is initialized using the ```dokusan``` package, with the difficulty controlled by the value of ```avg_rank```.
* The program chooses an empty square (represented as zeroes in a numpy array) and tries all the possible valid choices for that square until it finds one that works.
* If the chosen number leads to a consistent solution at that point in time, it moves on to the next square. If not, it revises the previous choice (backtracks) and repeats the process until the board is filled.

The game's UI works as follows:
* A GUI is created using ```pygame``` that tracks the time spent on the game, the number of incorrect choices made, and the placement of correct choices.
* If an incorrect choice is made, the square can be reverted to its blank state by hitting ```delete```.
* When the player has correctly guessed all the blank squares, the game is terminated and a message appears on the terminal.
