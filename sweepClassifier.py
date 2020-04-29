'''
@author: zy-f
'''

from sweepNet import *
import torch

class SweepClassifier(object):
    def __init__(self, net_kwargs, device='cpu'):
        self.net = SweepNet(**net_kwargs)
        self.loss_func = PolicyLoss()
        self.device = device
        # self.dset = None

    def train(self, batch, lr=1e-3, mini_bsz=32):
        self.optim = torch.optim.Adam(self.net.parameters(), lr=lr)
        
        states, actions, advantages = tuple(map(torch.Tensor, batch))
        actions = actions.long()

        k = 0
        while k+bsz 

        # self.net = default_train(self.net, self.dset, self.loss_func, self.optim, epochs=5, pred_y_func=None)
    
    def get_policy(self, state):
        state = torch.from_numpy(state, device=self.device).unsqueeze(0)
        self.net.test()
        out = self.net(state)
        return out.detach()[0]
        