import numpy as np
from random import randint


# places mines on a numpy array
def setmines(w, h, n):
    mines = np.zeros((h, w))
    for i in range(n):
        tempspace = (randint(0, h), randint(0, w))

if __name__ == '__main__':
    # information about board, depends on dificulty
    width = 16
    height = 16
    number = 40

    mines = setmines(width, height, number)
    board = np.zeros((height, width))