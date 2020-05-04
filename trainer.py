'''
@author: 20wang, zy-f
'''

from sweepClassifier import *
from aiAgent import *
from board import Board
import renderer

def play_game(agent, render=False):
    game_board = Board()
    reward = 0
    while True:
        _, a_play = agent.get_action(game_board.as_state(), learning=False)
        game_end, r = game_board.make_move(*a_play)
        reward += r
        if render:
            print(a_play)
            renderer.render(game_board)
        if game_end:
            if render:
                print("Total game reward:", reward)
            return reward

def train_sweeper(pretrained_path=None):
    net_kwargs = {
        'filter_list': [(5,50),(3,25)],
        'fc_dims': [288,220,220],
        'inp_layers':3,
        'board_dims': (6,6),
        'dropout': 0.05,
        'pool_size': None,
    }
    n_test_games = 10

    net = SweepClassifier(net_kwargs, cuda=True)
    if pretrained_path is not None:
        net.load_model(pretrained_path)
    print(net.model)
    agent = AIAgent(net)

    for i in range(80):
        print(f"=====TRAIN LOOP {i+1}=====")
        b = agent.make_batch(bsz=1000)
        net.train(b, lr=1e-4, batch_iters=2)
        torch.save(net.model.state_dict(), 'netsave.pth')

        reward = 0
        for k in range(n_test_games):
            reward += play_game(agent, render=False)
        if i % 10 == 0:
            play_game(agent, render=True)
        print(f"Average reward: {reward/n_test_games}")
    
    ### play game
    play_game(agent, render=True)

if __name__ == '__main__':
    train_sweeper(pretrained_path=None)