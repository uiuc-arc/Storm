import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
import torch.distributions.constraints as constraints
from pyro.infer import SVI
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
from pyro.contrib.autoguide import *
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
y= np.array([28.0, 8.0, -3.0, 7.0, -1.0, 1.0, 18.0, 12.0], dtype=np.float32).reshape(8,1)
y=torch.tensor(y)
J=8
J=torch.tensor(J)
sigma= np.array([15.0, 10.0, 16.0, 11.0, 9.0, 11.0, 10.0, 18.0], dtype=np.float32).reshape(8,1)
sigma=torch.tensor(sigma)
def model(y,J,sigma):
    mu = pyro.sample('mu'.format(''), dist.Normal(torch.tensor(1234.0)*torch.ones([amb(1)]),torch.tensor(1234.0)*torch.ones([amb(1)])))
    tau = pyro.sample('tau'.format(''), dist.Normal(torch.tensor(1234.0)*torch.ones([amb(1)]),torch.tensor(1234.0)*torch.ones([amb(1)])))
    with pyro.iarange('theta_range_'.format(''), J):
        theta = pyro.sample('theta'.format(''), dist.Normal(mu*torch.ones([amb(J)]),tau*torch.ones([amb(J)])))
    pyro.sample('obs__100'.format(), dist.Normal(theta,sigma), obs=y)
    
def guide(y,J,sigma):
    arg_1 = pyro.param('arg_1', torch.ones((amb(1))))
    arg_2 = pyro.param('arg_2', torch.ones((amb(1))), constraint=constraints.positive)
    mu = pyro.sample('mu'.format(''), dist.Normal(arg_1,arg_2))
    arg_3 = pyro.param('arg_3', torch.ones((amb(1))))
    arg_4 = pyro.param('arg_4', torch.ones((amb(1))), constraint=constraints.positive)
    tau = pyro.sample('tau'.format(''), dist.Normal(arg_3,arg_4))
    arg_5 = pyro.param('arg_5', torch.ones((amb(J))), constraint=constraints.positive)
    arg_6 = pyro.param('arg_6', torch.ones((amb(J))), constraint=constraints.positive)
    with pyro.iarange('theta_prange'):
        theta = pyro.sample('theta'.format(''), dist.Gamma(arg_5,arg_6))

    pass
optim = Adam({'lr': 0.05})
svi = SVI(model, guide, optim, loss=Trace_ELBO() if pyro.__version__ > '0.1.2' else 'ELBO')
for i in range(4000):
    loss = svi.step(y,J,sigma)
    if ((i % 1000) == 0):
        print(loss)
for name in pyro.get_param_store().get_all_param_names():
    print(('{0} : {1}'.format(name, pyro.param(name).data.numpy())))
print('mu_mean', np.array2string(dist.Normal(pyro.param('arg_1'), pyro.param('arg_2')).mean.detach().numpy(), separator=','))
print('theta_mean', np.array2string(dist.Gamma(pyro.param('arg_5'), pyro.param('arg_6')).mean.detach().numpy(), separator=','))
print('tau_mean', np.array2string(dist.Normal(pyro.param('arg_3'), pyro.param('arg_4')).mean.detach().numpy(), separator=','))
