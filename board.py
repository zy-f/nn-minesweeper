'''
@author: 20wang
'''

import numpy as np
from random import randrange


# represents a minesweeper board
class Board:
    def __init__(self, w, h, n):
        # information about board, depends on difficulty
        self.width = w
        self.height = h
        self.number = n
        self.blank = True

        # the board, as seen by the player
        self.play_board = np.full((h, w), -2)

        # randomly places mines on the board
        self.mine_map = np.zeros((h, w))
        mines = []
        i = 0
        while i < n:
            temp_space = (randrange(0, h), randrange(0, w))
            if temp_space not in mines:
                mines.append(temp_space)
                i += 1
        for mine in mines:
            self.mine_map[mine[0], mine[1]] = 1

    # changes the play board based on a "click"
    # click = 0 for left click, 1 for right click
    # returns true if the game is lost, false if not
    def make_move(self, x, y, click):

        if click == 1:
            self.play_board[y, x] = -1

        elif click == 0:
            # checks if game is lost

            if self.blank and self.mine_map[y, x] == 1.0:
                self.relocate_mine(y,x,y,x)

            if self.mine_map[y, x] == 1.0:
                self.play_board[y, x] = -3
                return True

            # checks adjacent squares for mines
            m = 0
            check_list = []
            for adj_x in range(-1, 2):
                for adj_y in range(-1, 2):
                    if 0 <= x + adj_x < self.width and 0 <= y + adj_y < self.height and not\
                            (adj_x == 0 and adj_y == 0):
                        check_list.append((y + adj_y, x + adj_x))


            if self.blank:
                    for c in check_list:
                        # first move, relocate the mine
                        self.relocate_mine(*c,y,x)

            for c in check_list:
                if self.mine_map[c[0], c[1]] == 1.0:
                    m += 1

            self.blank = False
            self.play_board[y, x] = m

            # auto-moves on zeroes if no adjacent mines, like real minesweeper does
            if m == 0:
                for c in check_list:
                    if self.play_board[c[0], c[1]] == -2:
                        self.make_move(c[1], c[0], 0)

        return False

    def relocate_mine(self,y,x,yi,xi):
        self.mine_map[y,x] = 0

        newx = randrange(0,self.width)
        newy = randrange(0,self.height)

        tries = 0
        while self.mine_map[newy, newx] == 1 or abs(newx-xi) < 2 or abs(newy-yi) < 2:
            newx = randrange(0, self.width)
            newy = randrange(0, self.height)

            tries += 1

            if tries > 100:
                print("Board is too small for successful relocation. Either expand board or decrease mines.")
                return

        self.mine_map[newy, newx] = 1


    # -3: there's a mine here and you lost
    # -2: unexplored space
    # -1: flagged space
    # 0+: number of mines adjacent to explored space
    def get_board(self):
        return self.play_board
