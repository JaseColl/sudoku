from dokusan import generators
import numpy as np

# Generate a Sudoku puzzle
arr = np.array(list(str(generators.random_sudoku(avg_rank=150))))
nums_str = arr.reshape(9, 9)
board = nums_str.astype('int').tolist()

def solve(sudoku):
    found = find_empty(sudoku)
    if not found:
        return True
    row, col = found

    for k in range(1, 10):
        if validate(sudoku, k, (row, col)):
            sudoku[row][col] = k
            if solve(sudoku):
                return True
            sudoku[row][col] = 0
    return False

def validate(sudoku, num, pos):
    row, col = pos
    # Check row
    if num in sudoku[row]:
        return False
    # Check column
    if num in [sudoku[i][col] for i in range(9)]:
        return False
    # Check 3x3 box
    box_x, box_y = col // 3, row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if sudoku[i][j] == num:
                return False
    return True

def print_board(sudoku):
    for i in range(len(sudoku)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(sudoku[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(sudoku[i][j])
            else:
                print(str(sudoku[i][j]) + " ", end="")
    print()

def find_empty(sudoku):
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                return (i, j)
    return None

# Example usage
print("Original Sudoku:")
print_board(board)
if solve(board):
    print("Solved Sudoku:")
    print_board(board)
else:
    print("No solution exists")
