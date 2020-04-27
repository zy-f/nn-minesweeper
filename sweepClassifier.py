'''
@author: zy-f
'''

from sweepNet import *

class SweepClassifier(object):
    def __init__(self, net_kwargs, device='cpu'):
        self.net = SweepNet(**net_kwargs)
        self.loss_func = PolicyLoss()
        self.device = device
        # self.dset = None

    def train(self, lr=1e-3):
        self.optim = torch.optim.Adam(self.net.parameters(), lr=lr)
        # self.net = default_train(self.net, self.dset, self.loss_func, self.optim, epochs=5, pred_y_func=None)
    
    def get_policy(self, state):
        state = torch.from_numpy(state, device=self.device).unsqueeze(0)
        self.net.test()
        out = self.net(state)
        return out.detach()[0]
        