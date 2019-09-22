from language.antlr.Template2Parser import Template2Parser, ParseTreeWalker
from language.antlr.Template2Listener import Template2Listener
from language.antlr.Template2Visitor import Template2Visitor

from utils.utils import *


class IndexMarker(Template2Listener):
    def __init__(self):
        self.tags = {}
        self.inindex = False

    def enterDims(self, ctx):
        if isinstance(ctx.parentCtx, Template2Parser.Array_accessContext):
            self.inindex = True
        elif isinstance(ctx.parentCtx, Template2Parser.DistexprContext):
            self.inindex = True
        elif isinstance(ctx.parentCtx, Template2Parser.DataContext):
            self.inindex = True

    def exitDims(self, ctx):
        self.inindex = False

    def enterArray_access(self, ctx):
        if self.inindex:
            self.tags[ctx.ID().getText()] = True

    def exitArray_access(self, ctx):
        self.inindex = False

    def enterRef(self, ctx):
        if self.inindex:
            self.tags[ctx.ID().getText()] = True

    @staticmethod
    def getIndices(node):
        marker = IndexMarker()
        walker = ParseTreeWalker()
        walker.walk(marker, node)
        return marker.tags


class PyroVisitor(Template2Visitor):
    def __init__(self, dtypes={}):
        self.models = parse_models()
        self.dtypes = dtypes
        self.curBlock = ""

    def visitUnary(self, ctx):
        return '-' + self.visit(ctx.expr())

    def visitFunction_call(self, ctx):
        func = ctx.FUNCTION().getText()
        func = self.functions[func]

        param_arr = []
        if ctx.params() is not None:
            for e in ctx.params().param():
                param_arr.append(self.visit(e))

        return func.format(*param_arr)

    def visitRef(self, ctx):
        return ctx.getText()

    def visitBrackets(self, ctx):
        return '(' + self.visit(ctx.expr()) + ')'

    def visitAddop(self, ctx):
        return self.visit(ctx.expr(0)) + "+" + self.visit(ctx.expr(1))

    def visitMinusop(self, ctx):
        return self.visit(ctx.expr(0)) + "-" + self.visit(ctx.expr(1))

    def visitDivop(self, ctx):
        return self.visit(ctx.expr(0)) + "/" + self.visit(ctx.expr(1))

    def visitMulop(self, ctx):
        if  isinstance(ctx.expr(0), Template2Parser.RefContext) and self.dtypes.get(ctx.expr(0).getText(), "") == 'matrix':
            return self.visit(ctx.expr(0)) + ".matmul(" + self.visit(ctx.expr(1)) +")"
        elif isinstance(ctx.expr(1), Template2Parser.RefContext) and self.dtypes.get(ctx.expr(1).getText(), "") == 'matrix':
            return self.visit(ctx.expr(0)) + ".matmul(" + self.visit(ctx.expr(1)) + ")"
        else:
            return self.visit(ctx.expr(0)) + "*" + self.visit(ctx.expr(1))

    def visitExponop(self, ctx):
        return self.visit(ctx.expr(0)) + "^" + self.visit(ctx.expr(1))

    
    
    
    def visitLeq(self, ctx):
        return self.visit(ctx.expr(0)) + '<=' + self.visit(ctx.expr(1))

    def visitAnd(self, ctx):
        return self.visit(ctx.expr(0)) + '&&' + self.visit(ctx.expr(1))

    def visitEq(self, ctx):
        return self.visit(ctx.expr(0)) + '==' + self.visit(ctx.expr(1))

    def visitGeq(self, ctx):
        return self.visit(ctx.expr(0)) + '>=' + self.visit(ctx.expr(1))

    def visitGt(self, ctx):
        return self.visit(ctx.expr(0)) + '>' + self.visit(ctx.expr(1))

    def visitLt(self, ctx):
        return self.visit(ctx.expr(0)) + '<' + self.visit(ctx.expr(1))

    def visitNe(self, ctx):
        return self.visit(ctx.expr(0)) + '!=' + self.visit(ctx.expr(1))

    def visitTernary(self, ctx):
        return self.visit(ctx.expr(1)) + 'if ' + self.visit(ctx.expr(0)) + ' else ' + self.visit(ctx.expr(2))

    def visitArray_access(self, ctx):
        return ctx.ID().getText() + "[" + self.visit(ctx.dims()) + "]"

    def visitDims(self, ctx):
        s = ''
        for d in ctx.expr():
            s += self.visit(d) + "-1,"
        return s[:-1]

    def visitDistexpr(self, ctx):
        
        dist = [x for x in self.models if x["name"] == ctx.ID().getText()][0]
        arg_str = ''

        
        
        
        
        
        
        args =[]
        for i in range(0, len(ctx.params().param())):
            arg = ctx.params().param(i).expr()
            exp = self.visit(arg)
            if isinstance(arg, Template2Parser.ValContext):
                args.append("Variable(({0})*torch.ones([1]))".format(exp))
            else:
                args.append(exp)
        for i in range(0, len(args)):
            a=args[i]
            if "pyro_args" in dist:
                arg_str += dist["pyro_args"][i]["name"] + "=" + str(a) + ","
            else:
                arg_str += str(a) + ","

        return dist["pyro"] + '(' + arg_str[:-1] + ')'

    def visitVal(self, ctx):
        return ctx.getText()

    functions = {
        "sqrt": "torch.sqrt({0})",
        "poisson_log": "torch.distributions.Poisson(torch.exp({0}))",
        "mean": "torch.mean({0})",
        "inv_cloglog": "(1-torch.exp(-torch.exp({0})))",
        "log": "torch.log({0})",
        "pi": "math.pi",
        "Phi": "dist.Normal(0,1).cdf({0})",
        "exp": "torch.exp({0})",
        "pow": "torch.pow({0}, {1})",
        "log1p": "torch.log(1+{0})",
        "lognormal_lpdf": "torch.log(dist.LogNormal({1},{2}).pdf({0}))",
        "pareto_lpdf": "torch.log(dist.Pareto({1},{2}).pdf({0}))",
        "diag_pre_multiply": "torch.diag({0})*{1}",
        "rep_val": "Variable(torch.Tensor([{0}]).repeat({1}))",
        "inverse": "torch.inverse({0})",
        "inv_logit": "(1/(1+torch.exp(-{0})))",
        "int_step": "(0 if {0} <= 0 else 1)",
        "fmax": "max({0}, {1})",
        "fmin": "min({0},{1})",
        "logit": "torch.log({0}/(1+{0}))",
        "sd": "torch.std({0})",
        "bernoulli_logit_lpmf": "torch.distributions.Bernoulli(logits={0}).log_prob({1})",
        "col": "{0}[:,{1}-1]",
        "if_else": "({1} if {0} else {2})",
        "fabs": "torch.abs({0})",
        "sum": "torch.sum({0})",
        "log10": "torch.log({0})",
        "rep_array": "Variable(torch.Tensor([{0}]).repeat({1}))",
        "to_vector": "{0}.view(-1)",
        "log1m": "torch.log(1-{0})",
        "rep_vector": "Variable(torch.tensor([{0}]).repeat({1}))"
    }


class PyroTranslator(Template2Listener):
    def __init__(self, algo='SVI', inv_post=False, betas=False, iters=4000):
        super(PyroTranslator, self).__init__()
        self.data = {}
        self.priors = {}
        self.models = parse_models()
        self.model = ""
        self.guide = ""
        self.tab = ""
        self.guide_tab = ""
        self.obs_index = []
        self.obs_string = []
        self.output_program = ""
        self.posteriors = {}
        self.queries = ""
        self.dtypes = {}
        self.transformedparamblk = ""
        self.curBlock = "model"
        self.nextint = 100
        self.initpriors = {}
        self.algo = algo  
        self.inv_post = inv_post 
        self.betas=betas
        self.iters=iters

    def addToCurBlock(self, code):
        if self.curBlock == "transformedparam":
            self.transformedparamblk += code
        else:
            self.model += code

    def parseArray(self, array):
        if array.array() is not None and len(array.array()) > 0:
            return np.array([self.parseArray(x) for x in array.array()])
        elif array.vector() is not None and len(array.vector()) > 0:
            return np.array([self.parseVector(x) for x in array.vector()])
        elif array.expr() is not None and len(array.expr()) > 0:
            
            if "." in array.getText():
                return np.array([np.float(x.getText()) for x in array.expr()])
            else:
                return np.array([np.int64(x.getText()) for x in array.expr()])
        else:
            print("Err:" + array.getText())

    def enterData(self, ctx):
        id = ctx.ID().getText()
        if ctx.array() is not None:
            arr = self.parseArray(ctx.array())
            self.data[id] = arr
            if ctx.array().vector() is not None and len(ctx.array().vector()) > 0:
                self.dtypes[id] = 'matrix'
            elif ctx.array().array() is not None and len(ctx.array().array()) > 0:
                self.dtypes[id] = 'matrix'
            else:
                self.dtypes[id] = 'arr'
        elif ctx.vector() is not None:
            arr = self.parseVector(ctx.vector())
            if ctx.vector().vector() is not None and len(ctx.vector().vector()) > 0:
                self.dtypes[id] = 'matrix'
            else:
                self.dtypes[id] = 'vector'
            self.data[id] = arr
        elif ctx.expr() is not None:
            if isinstance(ctx.expr(), Template2Parser.UnaryContext):
                number=ctx.expr().expr().number()
                self.data[id] = float(ctx.expr().getText()) if number.DOUBLE() is not None else np.int64(
                    ctx.expr().getText())
            elif ctx.expr().number() is not None:
                self.data[id] = float(ctx.expr().getText()) if ctx.expr().number().DOUBLE() is not None else np.int64(
                    ctx.expr().getText())

    def parseVector(self, vector):
        if vector.vector() is not None and len(vector.vector()) > 0:
            return np.array([self.parseVector(x) for x in vector.vector()])
        elif vector.array() is not None and len(vector.array()) > 0:
            return np.array([self.parseArray(x) for x in vector.array()])
        elif vector.expr() is not None and len(vector.expr()) > 0:
            
            if "." in vector.getText():
                return np.array([float(x.getText()) for x in vector.expr()])
            else:
                return np.array([int(x.getText()) for x in vector.expr()])
        else:
            print("Err:" + vector.getText())

    def enterPrior(self, ctx):
        name = ctx.expr().ID().getText()
        dist = ctx.distexpr()
        if '1234.0' in dist.getText():
            return

        if isinstance(ctx.expr(), Template2Parser.Array_accessContext):
            arrdim = ctx.expr().dims().getText()
            if name not in self.initpriors:
                _dims = dist.dims().getText() if dist.dims() is not None else '1'
                if dist.vectorDIMS() is not None:
                    if dist.dims() is not None:
                        _dims = dist.dims().getText() + "," + dist.vectorDIMS().dims().getText()
                    else:
                        _dims = dist.vectorDIMS().dims().getText()
                elif dist.dims() is not None:
                    _dims = dist.dims().getText()
                else:
                    _dims = '1'

                _dims = ','.join(['amb(' + p + ')' for p in _dims.strip().split(',') if len(p) > 0])
                self.initpriors[name] = '{0} = torch.zeros([{1}])'.format(name, _dims)
        else:
            arrdim = None

        prior = {"name": dist.ID().getText()}
        
        

        args = []
        for p in dist.params().param():
            if isinstance(p.expr(), Template2Parser.ValContext):
                
                
                args.append(
                    float(p.expr().getText()) if p.expr().number().DOUBLE() is not None else int(p.expr().getText()))
            elif isinstance(p.expr(), Template2Parser.RefContext):
                args.append(p.getText())
            else:
                args.append(PyroVisitor(self.dtypes).visit(p.expr()))

        prior["args"] = args
        prior['dims'] = dist.dims().getText() if dist.dims() is not None else None
        
        prior['vectordims'] = dist.vectorDIMS().dims().getText() if dist.vectorDIMS() is not None else None

        
        argslist = ''
        priorargs = []
        for arg in prior['args']:
            if isinstance(arg, (int, float)):
                v = "({0})".format(arg)
                
            elif isinstance(arg, np.ndarray):
                v = "({0})".format(np.array2string(arg, separator=','))
                
            else:
                
                v = str(arg)
                
            priorargs.append(v)
            argslist += v + ','

        prior['prior'] = [x for x in self.models if x['name'] == prior["name"]][0]

        
        placeholder = '_'.join(
            ['{' + str(i) + '}' for i in range(0, len(arrdim.split(",")))]) if arrdim is not None else ''
        if prior['vectordims'] is not None:
            self.model += self.tab + "with pyro.iarange('{0}_range_{2}'.format({1})):\n".format(name,
                                                                                                arrdim if arrdim is not None else '\'\'',
                                                                                                placeholder)
            if prior['dims'] is not None:

                
                
                
                
                dims = prior['dims'] + "," + prior['vectordims']

            else:
                dims = prior['vectordims']
            space = '    '
        else:
            if prior['dims'] is not None:
                dims = prior['dims']
                self.model += self.tab + "with pyro.iarange('{0}_range_{3}'.format({2}), {1}):\n".format(name,
                                                                                                         prior['dims'],
                                                                                                         arrdim if arrdim is not None else '\'\'',
                                                                                                         placeholder)
                space = '    '
            else:
                dims = '1'
                space = ''
        dims = ','.join(['amb(' + p + ')' for p in dims.strip().split(',') if len(p) > 0])
        if arrdim is not None:
            
            indices = arrdim.count(',') + 1

            
            arrdim = ','.join([p + '-1' for p in arrdim.split(',')])

            dims = ",".join(dims.split(",")[indices:])

        if 'pyro_args' in prior['prior']:
            curargs = ','.join(['{0}=Variable({1}*torch.ones([{2}]))'.format(b['name'], a, dims) for a, b in
                                zip(argslist[:-1].split(','), prior['prior']['pyro_args'])])
        else:
            curargs = ','.join(['Variable({0}*torch.ones([{1}]))'.format(a, dims) for a in argslist[:-1].split(',')])

        self.model += self.tab + space + "{0}{4} = pyro.sample('{1}{6}'.format({5}), {2}({3}))\n".format(name,
                                                                                                         name,
                                                                                                         prior['prior'][
                                                                                                             'pyro'],
                                                                                                         curargs,
                                                                                                         '[' + arrdim + ']' if arrdim is not None else '',
                                                                                                         arrdim if arrdim is not None else '\'\'',
                                                                                                         placeholder)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        if prior["prior"]["name"] == "categorical":
            posterior = prior["prior"]
        else:
            

            if self.inv_post:
                posterior_candidates = getUnSupportedDistributions(prior["prior"]["support"], pps="pyro012")
                posterior = np.random.choice([p for p in posterior_candidates if p['type'] == 'C' and p['name'] != "uniform"])
            else:
                posterior_candidates = getSupportedDistributions(prior["prior"]["support"], pps="pyro012")
                posterior = np.random.choice(
                    [p for p in posterior_candidates if p['type'] == 'C' and p["name"] in ["normal", "gamma"]] + [
                        prior["prior"]])
        arglist = ''
        args = []
        index = 0
        for arg in posterior["args"]:
            
            argname = get_new_var_name("arg_")
            try:
                float(prior["args"][0])
                dimn = 1
            except:
                dimn = 'len({0})'.format(priorargs[0])

            if prior["vectordims"] is not None:
                if prior["dims"] is not None:
                    dimn = prior["dims"] + "," + prior["vectordims"]
                else:
                    dimn = prior["vectordims"]
            elif prior["dims"] is not None:
                dimn = prior["dims"]
            else:
                dimn = '1'
            

            dimn = ','.join(['amb(' + p + ')' for p in dimn.strip().split(',') if len(p) > 0])

            if "dim" in arg and arg["dim"] == "pdm":
                
                
                self.guide += self.guide_tab + "{0} = pyro.param('{1}', Variable(torch.eye(({2})), requires_grad=True))\n".format(
                    argname, argname, dimn.count(',') + 1)
            elif is_positive(arg["type"]):
                self.guide += self.guide_tab + "{0} = torch.nn.Softplus()(pyro.param('{1}', Variable(torch.ones(({2})), requires_grad=True)))\n".format(
                    argname, argname, dimn)
            elif arg["type"] == "simplex":
                self.guide += self.guide_tab + "{0} = pyro.param('{1}', Variable(torch.ones(({2}))/{2}, requires_grad=True))\n".format(
                    argname, argname, dimn)
            else:
                self.guide += self.guide_tab + "{0} = pyro.param('{1}', Variable(torch.ones(({2})), requires_grad=True))\n".format(argname, argname,
                                                                                                     dimn)
            args.append(argname)
            if 'pyro_args' in prior['prior']:
                arglist += prior['prior']['pyro_args'][index]['name'] + "=" + argname + ","
            else:
                arglist += argname + ","
            index += 1

        if prior["dims"] is not None or prior["vectordims"] is not None:
            self.guide += self.guide_tab + "with pyro.iarange('{0}_prange'):\n".format(name)
            self.guide += self.guide_tab + "    {0}{4} = pyro.sample('{1}{6}'.format({5}), {2}({3}))\n".format(name,
                                                                                                               name,
                                                                                                               posterior[
                                                                                                                   'pyro'],
                                                                                                               arglist[
                                                                                                               :-1],
                                                                                                               '[' + arrdim + ']' if arrdim is not None else '',
                                                                                                               arrdim if arrdim is not None else '\'\'',
                                                                                                               placeholder)

        else:
            self.guide += self.guide_tab + "{0}{4} = pyro.sample('{1}{6}'.format({5}), {2}({3}))\n".format(name,
                                                                                                           name,
                                                                                                           posterior[
                                                                                                               'pyro'],
                                                                                                           arglist[:-1],
                                                                                                           '[' + arrdim + ']' if arrdim is not None else '',
                                                                                                           arrdim if arrdim is not None else '\'\'',
                                                                                                           placeholder)

        self.posteriors[name] = {"dist": posterior, "args": args, "dims": prior["dims"]}

    def enterDecl(self, ctx):
        
        if ctx.dtype().getText() == "vector":
            if len(ctx.dims()) > 1:
                d = ctx.dims(1).getText() + ", " + ctx.dims(0).getText()
            else:
                d = ctx.dims(0).getText()
            d=','.join(['amb(' + p + ')' for p in d.strip().split(',') if len(p) > 0])
            self.model += self.tab + "{0} = torch.zeros([{1}])\n".format(ctx.ID().getText(), d)
        elif ctx.dtype().getText() == "row_vector":
            if len(ctx.dims()) > 1:
                d = ctx.dims(1).getText() + ", " + ctx.dims(0).getText()
            else:
                d = ctx.dims(0).getText()
            d = ','.join(['amb(' + p + ')' for p in d.strip().split(',') if len(p) > 0])
            self.model += self.tab + "{0} = torch.zeros([{1}])\n".format(ctx.ID().getText(), d)
        elif ctx.dtype().getText() == "matrix":
            d =  ctx.dims(0).getText()
            d = ','.join(['amb(' + p + ')' for p in d.strip().split(',') if len(p) > 0])
            self.model += self.tab + "{0} = torch.zeros([{1}])\n".format(ctx.ID().getText(), d)
        elif ctx.dtype().getText() == "float" or ctx.dtype().getText() == "int":
            if ctx.dims() is not None and len(ctx.dims()) > 0:
                d = ctx.dims(0).getText()
            else:
                d = "1"
            d = ','.join(['amb(' + p + ')' for p in d.strip().split(',') if len(p) > 0])
            self.model += self.tab + "{0} = torch.zeros([{1}])\n".format(ctx.ID().getText(), d)

    def enterTransformeddata(self, ctx):
        self.curBlock = "transformeddata"

    def exitTransformeddata(self, ctx):
        self.curBlock = "model"

    def enterTransformedparam(self, ctx):
        self.curBlock = "transformedparam"

    def exitTransformedparam(self, ctx):
        self.curBlock = "model"

    def enterAssign(self, ctx):
        pv = PyroVisitor(self.dtypes)

        if ctx.ID() is not None:
            lhs = ctx.ID().getText()
        else:
            if len(ctx.expr()) > 1:
                lhs = pv.visit(ctx.expr(0))
            else:

                lhs = pv.visit(ctx.expr(0))
        if ctx.distexpr() is not None:
            rhs = pv.visit(ctx.distexpr())
        else:
            if len(ctx.expr()) > 1:
                rhs = pv.visit(ctx.expr(1))
            else:
                rhs = pv.visit(ctx.expr(0))
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        self.model += self.tab + lhs + "=" + rhs + "\n"

    def enterFor_loop(self, ctx=Template2Parser.For_loopContext):
        index = ctx.ID().getText()
        start = ctx.expr(0)
        end = ctx.expr(1)
        self.obs_index.append(index)
        self.obs_string.append('{' + str(len(self.obs_index) - 1) + '}')

        self.model += self.tab + "for {0} in range({1}, {2}+1):\n".format(index, PyroVisitor().visit(start),
                                                                          PyroVisitor().visit(end))
        
        self.guide += self.guide_tab + "for {0} in range({1}, {2}+1):\n".format(index, PyroVisitor().visit(start),
                                                                                PyroVisitor().visit(end))
        
        self.guide_tab += "    "
        self.tab += "    "

    def enterIf_stmt(self, ctx):
        self.model += self.tab + "if {0}:\n".format(PyroVisitor(self.dtypes).visit(ctx.expr()))
        self.tab += "    "

    def exitIf_stmt(self, ctx):
        self.tab = self.tab[:-4]

    def enterElse_blk(self, ctx):
        self.model += self.tab[:-4] + "else:\n"

    def enterObserve(self, ctx=Template2Parser.ObserveContext):
        import random
        random.randrange(10)

        if len(ctx.expr()) > 1:

            self.model += self.tab + 'pyro.sample(\'obs_{0}_{4}\'.format({1}), {2}, obs={3})\n'.format(
                '_'.join(self.obs_string),
                ','.join(self.obs_index),
                PyroVisitor(self.dtypes).visit(ctx.expr(0)),
                PyroVisitor(self.dtypes).visit(ctx.expr(1)),
                self.nextint)
        else:
            if 'binomial' in PyroVisitor(self.dtypes).visit(ctx.distexpr()).lower():
                convdouble = ".float()"
            elif 'bernoulli' in PyroVisitor(self.dtypes).visit(ctx.distexpr()).lower():
                convdouble = ".float()"  
            else:
                convdouble = ".float()"  
            convdouble = ""
            self.model += self.tab + 'pyro.sample(\'obs_{0}_{4}\'.format({1}), {2}, obs={3})\n'.format(
                '_'.join(self.obs_string),
                ','.join(self.obs_index),
                PyroVisitor(self.dtypes).visit(ctx.distexpr()),
                PyroVisitor(self.dtypes).visit(ctx.expr(0)) + convdouble,
                self.nextint)
        self.nextint += 1

    def exitFor_loop(self, ctx):
        self.tab = self.tab[:-4]
        self.guide += self.guide_tab + "pass\n"
        self.guide_tab = self.guide_tab[:-4]
        self.obs_index = self.obs_index[:-1]
        self.obs_string = self.obs_string[:-1]

    @staticmethod
    def _cast(arg, val):
        
        
        
        return "pyro.param('{0}')".format(val)

    def enterQuery(self, ctx):
        name = ctx.ID().getText()
        output = ""
        try:
            posterior = self.posteriors[name]
            if len(posterior["args"]) == 2:
                output += "print('{0}_mean', np.array2string({1}({2}, {3}).mean.detach().numpy(), separator=','))\n". \
                    format(name, posterior["dist"]["pyro"],
                           self._cast(posterior["dist"]["args"][0], posterior["args"][0]),
                           self._cast(posterior["dist"]["args"][1], posterior["args"][1]))
            else:
                output += "print('{0}_mean', np.array2string({1}({2}).mean.detach().numpy(), separator=','))\n". \
                    format(name,
                           posterior["dist"]["pyro"],
                           self._cast(posterior["dist"]["args"][0], posterior["args"][0]))
        except Exception as e:
            print(e)
            print(name + " not found")
        self.queries += output

    def exitTemplate(self, ctx):
        self.output_program = "import pyro, numpy as np, torch, pyro.distributions   as dist, torch.nn as nn\n"\
                              "from pyro.optim import Adam\n"\
                              "from pyro.infer import SVI\n" \
                              "from torch.autograd import Variable\n"\
                              "if pyro.__version__ > '0.1.2': from pyro.infer import Trace_ELBO\n"\
                              "import math\n"
        if self.algo == 'NUTS' or self.algo == 'HMC':
            self.output_program += "from pyro.infer.mcmc import HMC,NUTS,MCMC \n"

        
        self.output_program += "def amb(x):\n" \
                               "    return x.data.numpy().tolist() if isinstance(x, torch.Tensor) else x\n"
        
        indices = IndexMarker.getIndices(ctx)
        print("indices")
        print(indices)
        
        for data_key in self.data.keys():
            data_item = self.data[data_key]
            if isinstance(data_item, np.ndarray):
                
                datatype = 'np.int64' if data_item.dtype == np.int and data_key in indices else 'np.float32'
                
                
                
                
                
                self.output_program += data_key + "= np.array(" + str(data_item.tolist()) + ", dtype={0})\n".format(
                        datatype)
                self.output_program += data_key + "= Variable(torch.Tensor(" + data_key + "))\n"
            else:
                self.output_program += data_key + "=" + str(data_item) + "\n"
                if data_key in indices:
                    pass
                elif type(data_item) == np.int:
                    self.output_program += data_key + "= Variable(torch.Tensor(" + data_key + ", dtype=torch.int64))\n"
                else:
                    self.output_program += data_key + "= Variable(torch.Tensor(" + data_key + "))\n"

        self.output_program += "def model({0}):\n".format(",".join(self.data.keys()))
        
        for pr in self.initpriors:
            self.output_program += "    " + self.initpriors[pr] + "\n"
        
        self.output_program += "    " + self.model.replace("\n", "\n    ") + "\n"

        
        
        

        
        if self.algo == 'SVI':
            self.output_program += "def guide({0}):\n".format(",".join(self.data.keys()))
            
            for pr in self.initpriors:
                self.output_program += "    " + self.initpriors[pr] + "\n"
            
            self.output_program += "    " + self.guide.replace("\n", "\n    ") + "\n"

            self.output_program += "    pass\n"

            
            if self.betas:
                self.output_program += "optim = Adam({'lr': 0.05, 'betas':(1.0, 1.0)})\n"
            else:
                self.output_program += "optim = Adam({'lr': 0.05})\n"
            self.output_program += "svi = SVI(model, guide, optim, loss=Trace_ELBO() if pyro.__version__ > '0.1.2' else 'ELBO')\n"
            self.output_program += "for i in range({0}):\n".format(self.iters)
            self.output_program += "    loss = svi.step(" + ",".join(self.data.keys()) + ")\n"
            self.output_program += "    if ((i % 1000) == 0):\n"
            self.output_program += "        print(loss)\n"
            self.output_program += "for name in pyro.get_param_store().get_all_param_names():\n"
            self.output_program += "    print(('{0} : {1}'.format(name, pyro.param(name).data.numpy())))\n"
            self.output_program += self.queries
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

        elif self.algo == 'HMC':
            self.output_program += "hmc_kernel = HMC(model, step_size=0.0855, num_steps=4)\n" \
                                   "mcmc_run = MCMC(hmc_kernel, num_samples={1}, warmup_steps=100).run({0})\n".format(",".join(self.data.keys()), self.iters)
            for p in self.posteriors:
                self.output_program += "print(mcmc_run.marginal('{0}').empirical['{0}'].mean)\n".format(p)
        elif self.algo == 'NUTS':
            self.output_program += "hmc_kernel = NUTS(model)\n" \
                                   "mcmc_run = MCMC(hmc_kernel, num_samples={1}, warmup_steps=100).run({0})\n".format(",".join(self.data.keys()), self.iters)
            for p in self.posteriors:
                self.output_program += "print(mcmc_run.marginal('{0}').empirical['{0}'].mean)\n".format(p)
