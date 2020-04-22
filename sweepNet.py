'''
@author: zy-f
'''

import torch
import torch.nn as nn
import torch.nn.functional as F

class SweepNet(nn.Module):
    def __init__(self, filter_list=[(5,18),(3,36)], fc_dims=[288,220,220], inp_layers=2, board_dims=(6,6), dropout=.2, pool_size=3, dev='cpu'):
        super(SweepNet,self).__init__()
        board_size = np.prod(board_dims)
        self.dropout = nn.Dropout(dropout)
        self.n_conv_layers = len(filter_list)
        for k, (fsz, nf) in enumerate(filter_list):
            in_ch = inp_layers if k == 0 else getattr(self, f'conv{k}').out_channels
            setattr(self, f'conv{k+1}', nn.Conv2d(in_channels=in_ch, out_channels=nf, kernel_size=fsz, padding=fsz//2, device=dev)
        conv_output_size = filter_list[-1][-1]*board_size
        # MAX POOL?
        if pool_size:
            assert (np.array(board_dims) % pool_size == 0).all()
            self.max_pool = nn.MaxPool2d(pool_size)
            conv_output_size //= pool_size**2

        self.n_fc_layers = len(fc_dims)
        for k, out_ft in enumerate(fc_dims):
            in_ft = conv_output_size if k == 0 else getattr(self, f'fc{k}').out_features
            setattr(self, f'fc{k+1}', nn.Linear(in_ft, out_ft))
        self.fc_policy = nn.Linear(fc_dims[-1], board_size*2)
        self.softmax = nn.LogSoftmax(dim=-1)
    
    def forward(self, x):
        for k in range(self.n_conv_layers):
            x = self.dropout(F.relu(getattr(self, f'conv{k+1}')(x)))
        for k in range(self.n_fc_layers):
            x = self.dropout(F.relu(getattr(self, f'fc{k+1}')(x)))
        x = self.dropout(self.fc_policy(x))
        return self.softmax(x)
        
class PolicyLoss():
    pass