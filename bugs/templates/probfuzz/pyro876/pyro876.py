import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn
from pyro.optim import Adam
from pyro.infer import SVI
from torch.autograd import Variable
if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO
import math
def amb(x):
    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x
y= np.array([7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0], dtype=np.float32)
y= Variable(torch.Tensor(y))
x= np.array([66.51273632392986, 72.48109160982891, 51.593255272579405, 82.37396951614642, 24.351195093810894, 28.96641791103359, 99.38220110202795, 46.945634876575184, 74.85506975121858, 23.871686140356985, 42.81192218973854, 0.16365441832948413, 67.72794093186648, 1.5779302410995455, 85.61459094106726, 73.20330969160857, 97.22397591828582, 14.313599505994778, 77.26991866013726, 64.14754051119579, 93.5303981879472, 20.089351299968662, 85.04528490029601, 67.33599800099395, 86.68517663935083, 73.75596550033319, 44.8104798197569, 78.20407642948626, 26.66574964878745, 78.1633108272725, 58.678289830177086, 27.31380907315487, 4.02646194795423, 63.96186643228191, 49.082637268825046, 35.03886967734062, 58.61818429732906, 19.38738927550142, 98.52456832035858, 39.25739771133928, 60.79774433190946, 11.752239158453627, 57.486221669801516, 42.48732146320621, 92.4222761681774, 1.4253718046661978, 98.75835953068474, 37.249529584159546, 97.97336302377285, 94.2427128026267, 6.961615660785558, 32.09459629834591, 84.06976500181592, 19.70963412605615, 73.53560318406385, 3.5348040443181183, 63.37678085272886, 17.589970652899012, 23.756901561350062, 48.118915513262436, 13.310386313121093, 93.84208592206876, 42.0106423078408, 0.7016460089032894, 36.249000882381935, 48.097434185085696, 78.76424951716339, 45.02665818712342, 63.695720937909684, 57.593397718229724, 27.644987337721016, 35.2590623392631, 35.32549159337509, 54.3525304361895, 14.813294901937669, 85.34376122983905, 33.38578237754307, 13.190550838966153, 88.38295542333219, 1.4925274443232994, 13.659244846866613, 36.37151708656099, 10.993733689893459, 74.58947258034591, 30.702564887951855, 63.837945840218126, 32.7003556825763, 20.54693155899664, 10.189507990750712, 45.14291762207758, 93.83944291196097, 62.00878790146631, 31.72264988113014, 39.34175954482607, 39.484387340142455, 65.16948881524183, 0.29697889466003824, 73.20371542401847, 50.1177693144412, 89.14416693261028], dtype=np.float32)
x= Variable(torch.Tensor(x))
N=100
N= Variable(torch.Tensor(N))
def model(y,x,N):
    w = pyro.sample('w'.format(''), dist.Beta(Variable((21.217094954)*torch.ones([amb(1)])),Variable((86.1840115349)*torch.ones([amb(1)]))))
    b = pyro.sample('b'.format(''), dist.Gamma(Variable((23.8099134712)*torch.ones([amb(1)])),Variable((2.34475890762)*torch.ones([amb(1)]))))
    pyro.sample('obs__100'.format(), dist.Exponential(w*x+b), obs=y)

def guide(y,x,N):
    arg_1 = torch.nn.Softplus()(pyro.param('arg_1', Variable(torch.ones((amb(1))), requires_grad=True)))
    arg_2 = torch.nn.Softplus()(pyro.param('arg_2', Variable(torch.ones((amb(1))), requires_grad=True)))
    w = pyro.sample('w'.format(''), dist.Beta(arg_1,arg_2))
    arg_3 = torch.nn.Softplus()(pyro.param('arg_3', Variable(torch.ones((amb(1))), requires_grad=True)))
    arg_4 = torch.nn.Softplus()(pyro.param('arg_4', Variable(torch.ones((amb(1))), requires_grad=True)))
    b = pyro.sample('b'.format(''), dist.Gamma(arg_3,arg_4))

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
