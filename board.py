import numpy as np
from random import randrange


# places mines on a numpy array
def set_mines(w, h, n):
    mine_locations = np.zeros((h, w))
    mines = []

    i = 0
    while i < n:
        temp_space = (randrange(0, h), randrange(0, w))
        if temp_space not in mines:
            mines.append(temp_space)
            i += 1

    for mine in mines:
        mine_locations[mine[0], mine[1]] = 1

    return mine_locations


if __name__ == '__main__':
    # information about board, depends on dificulty
    width = 16
    height = 16
    number = 40

    mine_map = set_mines(width, height, number)
    board = np.zeros((height, width))

    
