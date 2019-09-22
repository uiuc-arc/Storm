import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
from pyro.infer import SVI
from torch.autograd import Variable
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
y= np.array([265.7134174564476, 62.48667853599276, 337.87234003772437, 269.2744730405883, 160.9550166078006, 243.92587454653545, 198.91151323303225, 83.18849820576311, 148.44213514725567, 97.03678075374569], dtype=np.float32)
y= Variable(torch.Tensor(y))
x= np.array([76.33124543997842, 16.039531213991985, 97.73878837569558, 77.38771146783661, 45.252345093060306, 69.86748817167427, 56.51298067528955, 22.18118463084988, 41.54012160726149, 26.289584432661805], dtype=np.float32)
x= Variable(torch.Tensor(x))
N=10
def model(y,x,N):
    w = pyro.sample('w'.format(''), dist.Beta(Variable(26.072914040168385*torch.ones([amb(1)])),Variable((42.3120851154)*torch.ones([amb(1)]))))
    with pyro.iarange('b_range_'.format(''), N):
        b = pyro.sample('b'.format(''), dist.Gamma(Variable((5.63887222899)*torch.ones([amb(N)])),Variable((40.1978121928)*torch.ones([amb(N)]))))
    with pyro.iarange('p_range_'.format(''), N):
        p = pyro.sample('p'.format(''), dist.Beta(Variable((52.1419233118)*torch.ones([amb(N)])),Variable((83.6618285099)*torch.ones([amb(N)]))))
    pyro.sample('obs__100'.format(), dist.Beta(w*x+b,p), obs=y)
    
def guide(y,x,N):
    arg_1 = torch.nn.Softplus()(pyro.param('arg_1', Variable(torch.ones((amb(1))), requires_grad=True)))
    arg_2 = torch.nn.Softplus()(pyro.param('arg_2', Variable(torch.ones((amb(1))), requires_grad=True)))
    w = pyro.sample('w'.format(''), dist.Beta(arg_1,arg_2))
    arg_3 = torch.nn.Softplus()(pyro.param('arg_3', Variable(torch.ones((amb(N))), requires_grad=True)))
    arg_4 = torch.nn.Softplus()(pyro.param('arg_4', Variable(torch.ones((amb(N))), requires_grad=True)))
    with pyro.iarange('b_prange'):
        b = pyro.sample('b'.format(''), dist.Gamma(arg_3,arg_4))
    arg_5 = torch.nn.Softplus()(pyro.param('arg_5', Variable(torch.ones((amb(N))), requires_grad=True)))
    arg_6 = torch.nn.Softplus()(pyro.param('arg_6', Variable(torch.ones((amb(N))), requires_grad=True)))
    with pyro.iarange('p_prange'):
        p = pyro.sample('p'.format(''), dist.Beta(arg_5,arg_6))
    
    pass
optim = Adam({'lr': 0.05})
svi = SVI(model, guide, optim, loss=Trace_ELBO() if pyro.__version__ > '0.1.2' else 'ELBO')
for i in range(4000):
    loss = svi.step(y,x,N)
    if ((i % 1000) == 0):
        print(loss)
for name in pyro.get_param_store().get_all_param_names():
    print(('{0} : {1}'.format(name, pyro.param(name).data.numpy())))
print('w_mean', np.array2string(dist.Beta(pyro.param('arg_1'), pyro.param('arg_2')).mean.detach().numpy(), separator=','))
print('b_mean', np.array2string(dist.Gamma(pyro.param('arg_3'), pyro.param('arg_4')).mean.detach().numpy(), separator=','))
print('p_mean', np.array2string(dist.Beta(pyro.param('arg_5'), pyro.param('arg_6')).mean.detach().numpy(), separator=','))
