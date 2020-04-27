"""
@author: 20nelson
"""


import numpy as np


def perform_rollout(net, board, limit=100):

    state = board.get_board()

    states = []
    actions = []
    rewards = []

    for n in range(limit):
        action = select_move(net, state)

        # are there any moves left?
        if action is None: break

        reward, done = board.step(*action) # does not actually exist yet :(

        states.append(state)
        actions.append(action)
        rewards.append(reward)

        state = board.get_board()

        if done: break

    return states, actions, rewards



def select_move(net, board):
    prediction = np.zeros(36)# net.predict(1d board) -> returns [p, ..., p] for each possible move, highest p is selected

    blacklist = []
    while True:
        highest = -1
        highestidx = -1

        if len(blacklist) == prediction.size:
            print("No more valid moves left!")
            return None

        for i in range(prediction.size):
            if i not in blacklist and abs(prediction[i]) > abs(highest):
                highest = prediction[i]
                highestidx = i

        # magically convert the selected index to a move. TODO
        move = (0,0,0)

        if compute_legality(*move, board):
            return move
        else:
            blacklist.append(highestidx)

def compute_legality(x, y, click, board):
    return board.get_board()[x][y] == -2