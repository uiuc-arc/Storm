import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
from pyro.infer import SVI
from torch.autograd import Variable
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
y= np.array([195.49070846212416, 866.7706832375152, 59.798078911494486, 453.71611095024736, 476.4467320500926, 830.7835855358135, 657.1794740774279, 705.7752514550402, 826.7969937567924, 45.39518602932701], dtype=np.float32)
y= Variable(torch.Tensor(y))
x= np.array([21.031906357042384, 94.21130327789396, 6.2394126580576525, 49.18227570188668, 51.66024794331937, 90.28817998254546, 71.36277678732014, 76.66043173760156, 89.85358280533039, 4.669285357023078], dtype=np.float32)
x= Variable(torch.Tensor(x))
N=10
def model(y,x,N):
    w = pyro.sample('w'.format(''), dist.Beta(Variable((32.571307843)*torch.ones([amb(1)])),Variable((19.8371500066)*torch.ones([amb(1)]))))
    with pyro.iarange('b_range_'.format(''), N):
        b = pyro.sample('b'.format(''), dist.Beta(Variable((90.6512046873)*torch.ones([amb(N)])),Variable((15.352380185)*torch.ones([amb(N)]))))
    with pyro.iarange('p_range_'.format(''), N):
        p = pyro.sample('p'.format(''), dist.Gamma(Variable((4.05626075528)*torch.ones([amb(N)])),Variable((69.1725232593)*torch.ones([amb(N)]))))
    cond=dist.Bernoulli(Variable((0.18846747694660726)*torch.ones([1])))
    if cond:
        pyro.sample('obs__100'.format(), dist.Beta(w*x+b,p), obs=y)
    else:
        pyro.sample('obs__101'.format(), dist.Beta(5.0*x+b,p), obs=y)
    pyro.sample('obs__102'.format(), dist.Beta(w*x+b,p), obs=y)
    pyro.sample('obs__103'.format(), dist.Beta(5.0*x+b,p), obs=y)
    
def guide(y,x,N):
    arg_1 = torch.nn.Softplus()(pyro.param('arg_1', Variable(torch.ones((amb(1))), requires_grad=True)))
    arg_2 = torch.nn.Softplus()(pyro.param('arg_2', Variable(torch.ones((amb(1))), requires_grad=True)))
    w = pyro.sample('w'.format(''), dist.Beta(arg_1,arg_2))
    arg_3 = torch.nn.Softplus()(pyro.param('arg_3', Variable(torch.ones((amb(N))), requires_grad=True)))
    arg_4 = torch.nn.Softplus()(pyro.param('arg_4', Variable(torch.ones((amb(N))), requires_grad=True)))
    with pyro.iarange('b_prange'):
        b = pyro.sample('b'.format(''), dist.Beta(arg_3,arg_4))
    arg_5 = torch.nn.Softplus()(pyro.param('arg_5', Variable(torch.ones((amb(N))), requires_grad=True)))
    arg_6 = torch.nn.Softplus()(pyro.param('arg_6', Variable(torch.ones((amb(N))), requires_grad=True)))
    with pyro.iarange('p_prange'):
        p = pyro.sample('p'.format(''), dist.Gamma(arg_5,arg_6))
    
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
print('b_mean', np.array2string(dist.Beta(pyro.param('arg_3'), pyro.param('arg_4')).mean.detach().numpy(), separator=','))
print('p_mean', np.array2string(dist.Gamma(pyro.param('arg_5'), pyro.param('arg_6')).mean.detach().numpy(), separator=','))
