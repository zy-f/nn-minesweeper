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
    
    def add_dirichlet_noise(self, p_distrib, noise=.05):
        noise_distrib = np.random.gamma(noise, 1, len(p_distrib))
        new_distrib = .75*p_distrib + .25*noise_distrib
        new_distrib /= np.sum(new_distrib)
        return new_distrib

    def get_action(self, s, learning=False, printing=False):
        policy = self.net.get_policy(s)
        if learning:
            policy = self.add_dirichlet_noise(policy)
        playable = np.vstack((s[-2],s[-1])).flatten()
        policy *= playable
        if np.max(policy) == 0 or np.isnan(policy).any():
            policy = playable/np.sum(playable)
        else:
            policy /= np.sum(policy)

        if learning:
            a = np.random.choice(range(len(policy)), p=policy)
        else:
            if printing:
                print(policy.reshape(s[-2:].shape))
            a = np.argmax(policy)
        a_play = (a % (len(policy)//2) % s.shape[1], a % (len(policy)//2) // s.shape[1], a // (len(policy)//2)) # x,y,click

        return a, a_play

    def get_advantage(self, rewards, limit, discount, epsilon=1e-12):
        returns = self.get_returns(rewards,limit,discount)
        mean = np.mean(returns,axis=0)
        adv = (returns - mean) / (np.std(returns, axis=0) + epsilon)
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