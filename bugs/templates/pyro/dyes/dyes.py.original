import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
import torch.distributions.constraints as constraints
from pyro.infer import SVI
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
from pyro.contrib.autoguide import *
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
y= np.array([[1545.0, 1540.0, 1595.0, 1445.0, 1595.0], [1520.0, 1440.0, 1555.0, 1550.0, 1440.0], [1630.0, 1455.0, 1440.0, 1490.0, 1605.0], [1595.0, 1515.0, 1450.0, 1520.0, 1560.0], [1510.0, 1465.0, 1635.0, 1480.0, 1580.0], [1495.0, 1560.0, 1545.0, 1625.0, 1445.0]], dtype=np.float32)
y=torch.tensor(y)
BATCHES=6
BATCHES=torch.tensor(BATCHES)
SAMPLES=5
SAMPLES=torch.tensor(SAMPLES)
def model(y,BATCHES,SAMPLES):
    theta = pyro.sample('theta'.format(''), dist.Normal(torch.tensor(0.0)*torch.ones([amb(1)]),torch.tensor(100000.0)*torch.ones([amb(1)])))
    tau_between = pyro.sample('tau_between'.format(''), dist.Gamma(torch.tensor(0.001)*torch.ones([amb(1)]),torch.tensor(0.001)*torch.ones([amb(1)])))
    tau_within = pyro.sample('tau_within'.format(''), dist.Gamma(torch.tensor(0.001)*torch.ones([amb(1)]),torch.tensor(0.001)*torch.ones([amb(1)])))
    sigma_between = torch.zeros([amb(1)])
    sigma_within = torch.zeros([amb(1)])
    sigma_between=1/torch.sqrt(tau_between)
    sigma_within=1/torch.sqrt(tau_within)
    with pyro.iarange('mu_range_'.format(''), BATCHES):
        mu = pyro.sample('mu'.format(''), dist.Normal(theta*torch.ones([amb(BATCHES)]),sigma_between*torch.ones([amb(BATCHES)])))
    for n in range(1, BATCHES+1):
        pyro.sample('obs_{0}_100'.format(n), dist.Normal(mu[n-1],sigma_within), obs=y[n-1])
    
def guide(y,BATCHES,SAMPLES):
    arg_1 = pyro.param('arg_1', torch.ones((amb(1))))
    arg_2 = pyro.param('arg_2', torch.ones((amb(1))), constraint=constraints.positive)
    theta = pyro.sample('theta'.format(''), dist.Normal(arg_1,arg_2))
    arg_3 = pyro.param('arg_3', torch.ones((amb(1))), constraint=constraints.positive)
    arg_4 = pyro.param('arg_4', torch.ones((amb(1))), constraint=constraints.positive)
    tau_between = pyro.sample('tau_between'.format(''), dist.Gamma(arg_3,arg_4))
    arg_5 = pyro.param('arg_5', torch.ones((amb(1))), constraint=constraints.positive)
    arg_6 = pyro.param('arg_6', torch.ones((amb(1))), constraint=constraints.positive)
    tau_within = pyro.sample('tau_within'.format(''), dist.Gamma(arg_5,arg_6))
    arg_7 = pyro.param('arg_7', torch.ones((amb(BATCHES))), constraint=constraints.positive)
    arg_8 = pyro.param('arg_8', torch.ones((amb(BATCHES))), constraint=constraints.positive)
    with pyro.iarange('mu_prange'):
        mu = pyro.sample('mu'.format(''), dist.Gamma(arg_7,arg_8))
    for n in range(1, BATCHES+1):
        pass

optim = Adam({'lr': 0.05})
svi = SVI(model, guide, optim, loss=Trace_ELBO() if pyro.__version__ > '0.1.2' else 'ELBO')
for i in range(4000):
    loss = svi.step(y,BATCHES,SAMPLES)
    if ((i % 1000) == 0):
        print(loss)
for name in pyro.get_param_store().get_all_param_names():
    print(('{0} : {1}'.format(name, pyro.param(name).data.numpy())))
print('mu_mean', np.array2string(dist.Gamma(pyro.param('arg_7'), pyro.param('arg_8')).mean.detach().numpy(), separator=','))
print('theta_mean', np.array2string(dist.Normal(pyro.param('arg_1'), pyro.param('arg_2')).mean.detach().numpy(), separator=','))
print('tau_within_mean', np.array2string(dist.Gamma(pyro.param('arg_5'), pyro.param('arg_6')).mean.detach().numpy(), separator=','))
print('tau_between_mean', np.array2string(dist.Gamma(pyro.param('arg_3'), pyro.param('arg_4')).mean.detach().numpy(), separator=','))
