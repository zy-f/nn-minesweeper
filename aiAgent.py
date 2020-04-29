'''
@author: zy-f
'''

from board import Board
# from sweepClassifier import SweepClassifier

class AIAgent(object):
    def __init__(self, net):
        self.net = net

    def get_action(self, s, learning=False):
        policy = self.net.get_policy(s)
        playable = np.vstack((s[1],s[1])).flatten()
        policy *= playable
        policy /= np.sum(policy)

        if learning:
            a = np.random.choice(range(len(policy)), p=policy)
        else:
            a = np.argmax(policy)
        a_play = (a % (len(policy)//2) // s.shape[1], a % (len(policy)//2) % s.shape[1], a // (len(policy)//2)) # x,y,click
        return a, a_play

    def simulate_game(self, max_turns=36):
        timesteps = 0
        states = []
        actions = []
        rewards = []
        b = Board()
        for k in range(max_turns):
            a, a_play = self.get_action(b.as_state(), learning=True)
            r, game_end = b.make_move(*a_play)

            timesteps += 1

            states.append(b.as_state())
            actions.append(a)
            rewards.append(r)

            if game_end:
                break

        return states, actions, rewards, timesteps

    def make_batch(self, bsz=200, max_turns=36):
        states = []
        actions = []
        rewards = []
        timesteps = 0
        while timesteps < bsz:
            max_turns = min(max_turns, bsz-timesteps)
            s,a,r,t = self.simulate_game(max_turns)
            timesteps += t
            states.append(s)
            actions.append(a)
            rewards.append(r)