import pystan
import pickle
from hashlib import md5
import json
import subprocess as sp
import datetime

def StanModel_cache(model_code, rebuild=False):
    code_hash = md5(model_code.encode('ascii')).hexdigest()

    cache_fn = 'cached-model-{}.pkl'.format(code_hash)
    try:
        if not rebuild:
            sm = pickle.load(open(cache_fn, 'rb'))
        else:
            raise FileNotFoundError
    except:
        sm = pystan.StanModel(file=model_code)
        #with open(cache_fn, 'wb') as f:
        #    pickle.dump(sm, f)
    else:
        print("Using cached StanModel")
    return sm


import sys

if len(sys.argv) > 1:
    inf_type = sys.argv[1]
else:
    inf_type ='hmc'
params = False
rebuild = False
if len(sys.argv) > 2:
    iterations = int(sys.argv[2])
else:
    iterations = 1000

sm = StanModel_cache('stan543.stan', rebuild)
with open('stan543.json') as dataFile:
    data = json.load(dataFile)
start = datetime.datetime.now()
try:
    if inf_type == 'sampling':
        fit = sm.sampling(data=data, iter=iterations, chains=4)
        print(fit)

    elif inf_type == 'hmc':
        fit = sm.sampling(data=data, iter=iterations, chains=4, algorithm='HMC')
        print(fit)

    elif inf_type == 'vb':
        fit = sm.vb(data=data, iter=1000)
        print(fit['args']['sample_file'])

except (RuntimeError,ValueError) as err:
    print(err)

end=datetime.datetime.now()
print(end-start)