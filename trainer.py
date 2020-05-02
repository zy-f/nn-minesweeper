'''
@author: 20wang, zy-f
'''

from sweepClassifier import *
from aiAgent import *
from board import Board
import renderer

def train_sweeper():
    net_kwargs = {
        'filter_list': [(5,18),(3,36)],
        'fc_dims': [288,220,220],
        'inp_layers':3,
        'board_dims': (6,6),
        'dropout': .2,
        'pool_size': None,
    }

    net = SweepClassifier(net_kwargs, cuda=True)
    print(net.model)
    agent = AIAgent(net)

    for i in range(50):
        print(f"=====TRAIN LOOP {i+1}=====")
        b = agent.make_batch()
        net.train(b)
        torch.save(net.model, 'netsave.pth')
    
    ### play game
    game_board = Board()
    k = 0
    while True:
        _, a_play = agent.get_action(game_board.as_state(), learning=False)
        print(a_play)
        game_end, _ = game_board.make_move(*a_play)
        renderer.render(game_board)
        if game_end:
            break

if __name__ == '__main__':
    train_sweeper()