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
        _, a_play = agent.get_action(game_board.as_state(), learning=True, printing=False)
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
        'inp_layers': 3,
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

    best_avg_reward = -float('inf')
    for i in range(int(5e3)):
        if i%10==0:
            print(f"=====TRAIN LOOP {i+1}=====")
        b = agent.make_batch(bsz=200)
        net.train(b, lr=1e-4, batch_iters=1, mini_bsz=200, printing=(i%10==0), load_best=None)

        reward = 0
        for k in range(n_test_games):
            reward += play_game(agent, render=False)
        avg_reward = reward/n_test_games
        if avg_reward > best_avg_reward:
            best_avg_reward = avg_reward
            torch.save(net.model.state_dict(), 'netsave2.pth')
        if i % 10 == 0:
            play_game(agent, render=True)
            print(f"Avg reward: {avg_reward}, best avg reward: {best_avg_reward}")
    
    ### play game
    agent.net.load_model('netsave2.pth')
    play_game(agent, render=True)

if __name__ == '__main__':
    train_sweeper(pretrained_path=None)