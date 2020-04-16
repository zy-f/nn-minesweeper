'''
@author: cpolzak
'''
from sweepNet import SweepNet

def convert_board(board):
        b = board.get_board()
        net_board = np.empty((2,)+b.shape,dtype=np.float32)
        net_board[0,:,:] = np.maximum(b,0)
        net_board[1,:,:] = (b>=0)
        return net_board

class SweepClassifier(object):
    def __init__(self, net_kwargs):
        self.net = SweepNet(**net_kwargs)
        self.dset = None

    def train(self):
        pass
        