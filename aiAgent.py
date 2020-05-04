'''
@author: zy-f, trevnels
'''
import renderer
from board import Board
import numpy as np
# from sweepClassifier import SweepClassifier

class AIAgent(object):
    def __init__(self, net):
        self.net = net

    def get_action(self, s, learning=False):
        policy = self.net.get_policy(s)
        # print(s)
        playable = np.vstack((s[1],s[2])).flatten()
        policy *= playable
        temp_policy = policy
        policy /= np.sum(policy)

        try:
            if learning:
                a = np.random.choice(range(len(policy)), p=policy)
            else:
                a = np.argmax(policy)
            a_play = (a % (len(policy)//2) % s.shape[1], a % (len(policy)//2) // s.shape[1], a // (len(policy)//2)) # x,y,click

            return a, a_play
        except:
            print("Predivided policy:")
            print(temp_policy)
            print("Divided policy:")
            print(policy)
            0/0


    def get_advantage(self, rewards, limit, discount, epsilon=1e-12):
        returns = self.get_returns(rewards,limit,discount)
        mean = np.mean(returns,axis=0)
        adv = (returns - mean*(mean>0)) / (np.std(returns, axis=0) + epsilon)
        adv = [a[:len(rewards[i])] for i, a in enumerate(adv)]
        return adv

    def get_returns(self, rewards, limit, discount):
        returns = np.zeros((len(rewards), limit))
        for i, re in enumerate(rewards):
            returns[i, len(re)-1] = re[-1]
            for j in reversed(range(len(re)-1)):
                returns[i,j] = re[j] + discount * returns[i,j+1]
        return returns

    def simulate_game(self, max_turns=36):
        timesteps = 0
        states = []
        actions = []
        rewards = []
        b = Board()
        # print("New game")
        for k in range(max_turns):
            a, a_play = self.get_action(b.as_state(), learning=True)
            game_end, r = b.make_move(*a_play)
            # print(a_play)
            # renderer.render(b)

            timesteps += 1

            states.append(b.as_state())
            actions.append(a)
            rewards.append(r)

            if game_end:
                break

        return states, actions, rewards, timesteps

    def make_batch(self, bsz=200, max_turns=36, discount = 0.0):
        states = []
        actions = []
        rewards = []
        timesteps = 0
        while timesteps < bsz:
            turns = min(max_turns, bsz-timesteps)
            s,a,r,t = self.simulate_game(turns)
            timesteps += t
            states.append(s)
            actions.append(a)
            rewards.append(r)

        adv = self.get_advantage(rewards, max_turns, discount)

        statelist = [item for s in states for item in s]
        actlist = [item for s in actions for item in s]
        advlist = [item for s in adv for item in s]

        return np.array(statelist, dtype=np.float32), np.array(actlist, dtype=np.int64), np.array(advlist, dtype=np.float32)