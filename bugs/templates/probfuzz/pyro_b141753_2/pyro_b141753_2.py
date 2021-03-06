import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
from pyro.infer import SVI
from torch.autograd import Variable
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
y= np.array([2.992050578947774, 1.9485827497324826, 2.773794578170376, 2.9219837778575517, 2.0456465303908, 1.2203309210706872, 1.9816272088661024, 2.0043992881660087, 1.903000031419428, 2.9114229974103054], dtype=np.float32)
y= Variable(torch.Tensor(y))
x= np.array([72.9668288804832, 34.9411912478001, 65.0132309214918, 70.41348251585046, 38.478350753088385, 8.402529137960668, 36.14538422203676, 36.97523523550993, 33.28008404319335, 70.02863077518174], dtype=np.float32)
x= Variable(torch.Tensor(x))
N=10
def model(y,x,N):
    w = pyro.sample('w'.format(''), dist.Exponential(Variable((37.4790187832)*torch.ones([amb(1)]))))
    with pyro.iarange('b_range_'.format(''), N):
        b = pyro.sample('b'.format(''), dist.Exponential(Variable(31.494555467732837*torch.ones([amb(N)]))))
    with pyro.iarange('p_range_'.format(''), N):
        p = pyro.sample('p'.format(''), dist.Normal(Variable(55.43075391668968*torch.ones([amb(N)])),Variable((61.3521758404)*torch.ones([amb(N)]))))
    pyro.sample('obs__100'.format(), dist.LogNormal(w*x+b,p), obs=y)
    
def guide(y,x,N):
    arg_1 = torch.nn.Softplus()(pyro.param('arg_1', Variable(torch.ones((amb(1))), requires_grad=True)))
    w = pyro.sample('w'.format(''), dist.Exponential(arg_1))
    arg_2 = torch.nn.Softplus()(pyro.param('arg_2', Variable(torch.ones((amb(N))), requires_grad=True)))
    arg_3 = torch.nn.Softplus()(pyro.param('arg_3', Variable(torch.ones((amb(N))), requires_grad=True)))
    with pyro.iarange('b_prange'):
        b = pyro.sample('b'.format(''), dist.Gamma(arg_2,arg_3))
    arg_4 = pyro.param('arg_4', Variable(torch.ones((amb(N))), requires_grad=True))
    arg_5 = torch.nn.Softplus()(pyro.param('arg_5', Variable(torch.ones((amb(N))), requires_grad=True)))
    with pyro.iarange('p_prange'):
        p = pyro.sample('p'.format(''), dist.Normal(arg_4,arg_5))
    
    pass
optim = Adam({'lr': 0.05})
svi = SVI(model, guide, optim, loss=Trace_ELBO() if pyro.__version__ > '0.1.2' else 'ELBO')
for i in range(4000):
    loss = svi.step(y,x,N)
    if ((i % 1000) == 0):
        print(loss)
for name in pyro.get_param_store().get_all_param_names():
    print(('{0} : {1}'.format(name, pyro.param(name).data.numpy())))
print('w_mean', np.array2string(dist.Exponential(pyro.param('arg_1')).mean.detach().numpy(), separator=','))
print('b_mean', np.array2string(dist.Gamma(pyro.param('arg_2'), pyro.param('arg_3')).mean.detach().numpy(), separator=','))
print('p_mean', np.array2string(dist.Normal(pyro.param('arg_4'), pyro.param('arg_5')).mean.detach().numpy(), separator=','))
