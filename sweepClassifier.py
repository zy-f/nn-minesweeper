'''
@author: zy-f
'''

from sweepNet import *
import torch

class SweepClassifier(object):
    def __init__(self, net_kwargs, cuda=True):
        self.device = torch.device('cuda:0' if cuda and torch.cuda.is_available() else 'cpu')
        self.model = SweepNet(**net_kwargs).to(self.device)
        self.loss_func = PolicyLoss()

    def train(self, batch, lr=1e-3, mini_bsz=32):
        self.model.train()
        self.optim = torch.optim.Adam(self.model.parameters(), lr=lr)
        states, actions, advantages = batch
        states = torch.from_numpy(states).to(self.device)
        actions = torch.from_numpy(actions).to(self.device)
        advantages = torch.from_numpy(advantages).to(self.device)

        k = 0
        loss_size = 0.0
        while k+mini_bsz < len(states):
            out = self.model(states[k:k+mini_bsz])
            loss = self.loss_func(out, actions[k:k+mini_bsz], advantages[k:k+mini_bsz])
            loss.backward()
            self.optim.step()
            loss_size += loss.item()
            k += mini_bsz
        loss_size /= k//mini_bsz
        print(f"Loss: {loss_size}")
    
    def get_policy(self, state):
        state = torch.from_numpy(state).unsqueeze(0).to(self.device)
        self.model.eval()
        out = self.model(state)
        return out.detach().to('cpu').numpy()[0]
        