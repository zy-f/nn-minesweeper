'''
@author: zy-f
'''
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class SweepNet(nn.Module):
    def __init__(self, filter_list=[(5,18),(3,36)], fc_dims=[288,220,220], inp_layers=2, board_dims=(6,6), dropout=.2, pool_size=3):
        super(SweepNet,self).__init__()
        board_size = np.prod(board_dims)
        self.dropout = nn.Dropout(dropout)
        self.n_conv_layers = len(filter_list)
        for k, (fsz, nf) in enumerate(filter_list):
            in_ch = inp_layers if k == 0 else getattr(self, f'conv{k}').out_channels
            setattr(self, f'conv{k+1}', nn.Conv2d(in_channels=in_ch, out_channels=nf, kernel_size=fsz, padding=fsz//2))
        conv_output_size = filter_list[-1][-1]*board_size
        # MAX POOL?
        self.pool_size = pool_size
        if pool_size:
            assert (np.array(board_dims) % pool_size == 0).all()
            self.max_pool = nn.MaxPool2d(pool_size)
            conv_output_size //= pool_size**2

        self.n_fc_layers = len(fc_dims)
        for k, out_ft in enumerate(fc_dims):
            in_ft = conv_output_size if k == 0 else getattr(self, f'fc{k}').out_features
            setattr(self, f'fc{k+1}', nn.Linear(in_ft, out_ft))
        self.fc_policy = nn.Linear(fc_dims[-1], board_size*2) # left half = reveal square, right half = flag as mine
        self.softmax = nn.Softmax(dim=-1)
    
    def forward(self, x):
        for k in range(self.n_conv_layers):
            x = self.dropout(F.relu(getattr(self, f'conv{k+1}')(x)))
        if self.pool_size:
            x = self.max_pool(x)
        x = x.view(x.shape[0], -1) # flatten
        for k in range(self.n_fc_layers):
            x = self.dropout(F.relu(getattr(self, f'fc{k+1}')(x)))
        x = self.dropout(self.fc_policy(x))
        return self.softmax(x)

class PolicyLoss(nn.Module):
    def __init__(self):
        super(PolicyLoss, self).__init__()

    def forward(self, policy, action, advantage, epsilon=1e-12):
        # advantage ~= reward - baseline
        policy_slice = policy.gather(1, action.view(-1,1))
        loss = - (torch.log(policy_slice+epsilon) * (advantage>0) + torch.log(1-policy_slice+epsilon) * (advantage<0)).mean()
        return loss
