import pygame
from dokusan import generators
import numpy as np
from sudoku_solver import solve, validate
import time

pygame.font.init()

class Grid:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.board = np.array(list(str(generators.random_sudoku(avg_rank=10000)))).reshape(9, 9).astype('int')
        self.cubes = [[UnitCube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, value):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(value)
            self.update_model()
            if validate(self.model, value, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, value):
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def draw(self, win):
        gap = self.width / 9
        for i in range(self.rows + 1):
            thick = 4 if i % 3 == 0 and i != 0 else 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for row in self.cubes:
            for cube in row:
                cube.draw(win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        return None

    def is_finished(self):
        return all(self.cubes[i][j].value != 0 for i in range(self.rows) for j in range(self.cols))


class UnitCube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, play_time, strikes):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("timesnewroman", 40)
    time_text = fnt.render("Time: " + time_secs_format(play_time), 1, (0, 0, 0))
    win.blit(time_text, (540 - 160, 560))
    strikes_text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(strikes_text, (20, 560))
    board.draw(win)


def time_secs_format(secs):
    minute, sec = divmod(secs, 60)
    return f" {minute}:{sec}"


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku!")
    board = Grid(9, 9, 540, 540)
    key = None
    running = True
    start = time.time()
    strikes = 0

    while running:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_1, pygame.K_10):
                    key = event.key - pygame.K_0
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN and board.selected:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Correct!")
                        else:
                            print("Incorrect, try again.")
                            strikes += 1
                        key = None
                        if board.is_finished():
                            print("You win!")
                            running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(*clicked)
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
