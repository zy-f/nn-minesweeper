'''
@author: 20wang, zy-f
'''

from sweepClassifier import *
from aiAgent import *

if __name__ == '__main__':
    net_kwargs = {
        'filter_list': [(5,18),(3,36)],
        'fc_dims': [288,220,220],
        'inp_layers':2,
        'board_dims': (6,6),
        'dropout': .2,
        'pool_size': 3,
        'cuda': True
    }

    net = SweepClassifier(net_kwargs)
    agent = AIAgent(net)

    for i in range(10):
        print(f"=====TRAIN LOOP {i+1}=====")
        b = agent.make_batch()
        net.train(b)
        torch.save(net.model, 'netsave.pth')