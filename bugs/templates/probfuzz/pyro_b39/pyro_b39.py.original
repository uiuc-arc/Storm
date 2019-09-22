import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
from pyro.infer import SVI
from torch.autograd import Variable
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
y= np.array([23672.645110996596, 15550.559142204569, 25258.808657188703, 26982.472622640067, 32514.29840747452, 36837.3583193422, 20836.713321071216, 15132.693800834739, 30555.45610141966, 18073.517500231846], dtype=np.float32)
y= Variable(torch.Tensor(y))
x= np.array([[23.615982475803076, 29.918019356158045, 94.48454200540873, 10.94666807273843, 78.75624937437861, 79.3129813897252, 18.250127006756124, 3.0734059171176664, 31.222953589257063, 2.981825264801874], [36.413041473857874, 33.859890188064945, 69.49871899265729, 71.6623077381701, 99.62027160230393, 92.06767616983538, 91.70604899913269, 16.081848374399467, 99.54821309518637, 40.53002544242449], [26.441209275227852, 44.732740341821874, 81.42111659745817, 12.30957474281471, 19.360064988133786, 26.187852842797977, 11.984129879788696, 61.448797474523, 40.48130120482036, 55.26412061367676], [51.922710025994334, 3.4685648120755697, 47.70289555096047, 96.71891822806249, 33.102815565182354, 95.23014369947822, 29.66509361304508, 62.86750575739132, 38.035035521382234, 62.59468464035097], [49.98843350271134, 70.18305109971844, 60.924663446314774, 76.11984303247591, 81.14387496580689, 8.40784753289887, 62.32907832578238, 4.150703434190717, 94.71961686305721, 24.149970765089467], [73.18346165355598, 6.626270061143225, 46.03809777384971, 89.76895724420774, 56.07885353079186, 90.67566566543923, 25.85969756877653, 61.142420984834764, 98.92160303886621, 15.487590409154794], [85.68335807897584, 57.1459940656443, 71.16522475318541, 96.04484836828155, 37.21324839463874, 31.559072593568725, 1.1143648594463929, 9.063487944675696, 97.37111231014576, 81.93299436795176], [98.91195932415732, 94.86584877197495, 39.53981017733218, 83.95417034928462, 65.85766618979385, 72.82843163802035, 31.37712719454243, 91.34454122013624, 21.407267499222428, 29.15302265739369], [61.307557209773776, 38.12880241860624, 12.060317430275713, 14.806798497123541, 82.33778446888856, 66.16715998879779, 65.69763212513546, 26.58332112086371, 44.78802048131049, 34.52724113689608], [18.749811887076383, 70.95076093322668, 36.66039571524708, 46.80958753731368, 64.1204763591165, 73.87340425393268, 40.54188705863455, 8.966243692374176, 44.91675811254455, 89.62186147395275]], dtype=np.float32)
x= Variable(torch.Tensor(x))
N=10
N= Variable(torch.Tensor(N))
def model(y,x,N):
    with pyro.iarange('w_range_'.format(''), 10):
        w = pyro.sample('w'.format(''), dist.Beta(Variable((96.3839819806)*torch.ones([amb(10)])),Variable((64.1469739463)*torch.ones([amb(10)]))))
    b = pyro.sample('b'.format(''), dist.LogNormal(Variable(58.4973357440217*torch.ones([amb(1)])),Variable((9.77400737468)*torch.ones([amb(1)]))))
    with pyro.iarange('p_range_'.format(''), 10):
        p = pyro.sample('p'.format(''), dist.Beta(Variable((88.4814395817)*torch.ones([amb(10)])),Variable((25.1426926938)*torch.ones([amb(10)]))))
    pyro.sample('obs__100'.format(), dist.Beta(w.matmul(x)+b,p), obs=y)
    
def guide(y,x,N):
    arg_1 = torch.nn.Softplus()(pyro.param('arg_1', Variable(torch.ones((amb(10))), requires_grad=True)))
    arg_2 = torch.nn.Softplus()(pyro.param('arg_2', Variable(torch.ones((amb(10))), requires_grad=True)))
    with pyro.iarange('w_prange'):
        w = pyro.sample('w'.format(''), dist.Beta(arg_1,arg_2))
    arg_3 = pyro.param('arg_3', Variable(torch.ones((amb(1))), requires_grad=True))
    arg_4 = torch.nn.Softplus()(pyro.param('arg_4', Variable(torch.ones((amb(1))), requires_grad=True)))
    b = pyro.sample('b'.format(''), dist.LogNormal(arg_3,arg_4))
    arg_5 = torch.nn.Softplus()(pyro.param('arg_5', Variable(torch.ones((amb(10))), requires_grad=True)))
    arg_6 = torch.nn.Softplus()(pyro.param('arg_6', Variable(torch.ones((amb(10))), requires_grad=True)))
    with pyro.iarange('p_prange'):
        p = pyro.sample('p'.format(''), dist.Beta(arg_5,arg_6))
    
optim = Adam({'lr': 0.05})
svi = SVI(model, guide, optim, loss=Trace_ELBO() if pyro.__version__ > '0.1.2' else 'ELBO')
for i in range(4000):
    loss = svi.step(y,x,N)
    if ((i % 1000) == 0):
        print(loss)
for name in pyro.get_param_store().get_all_param_names():
    print(('{0} : {1}'.format(name, pyro.param(name).data.numpy())))
print('w_mean', np.array2string(dist.Beta(pyro.param('arg_1'), pyro.param('arg_2')).mean.detach().numpy(), separator=','))
print('b_mean', np.array2string(dist.LogNormal(pyro.param('arg_3'), pyro.param('arg_4')).mean.detach().numpy(), separator=','))
print('p_mean', np.array2string(dist.Beta(pyro.param('arg_5'), pyro.param('arg_6')).mean.detach().numpy(), separator=','))
with open('pyro_out', 'w') as outputfile:
    outputfile.write('b, lognormal,{0},{1}\n'.format(pyro.param('arg_3').detach().numpy(),pyro.param('arg_4').detach().numpy()))
