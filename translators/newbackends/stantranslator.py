from language.antlr.Template2Lexer import Template2Lexer
from language.antlr.Template2Parser import Template2Parser
from language.antlr.Template2Listener import Template2Listener
from language.antlr.Template2Visitor import Template2Visitor
import antlr4
import six
from utils.utils import *
from antlr4 import *
import subprocess as sp


class StanVisitor(Template2Visitor):
    def __init__(self, dtypes={}, functions={}):
        self.models = parse_models()
        self.dtypes = dtypes
        self.functions = functions

    def visitRef(self, ctx):
        return ctx.getText()

    def visitString(self, ctx):
        return ctx.getText()

    def visitTranspose(self, ctx):
        return self.visit(ctx.expr()) + "'"

    def visitDtype(self, ctx=Template2Parser.DtypeContext):
        if ctx.primitive() is not None:
            if ctx.dims() is not None:
                ctx.getText().replace('float', 'real') + '[' + self.visit(ctx.dims()) + ']'
            else:
                return ctx.getText().replace('float', 'real')
        elif ctx.COMPLEX() is not None:
            return ctx.COMPLEX().getText()

    def visitReturn_or_param_type(self, ctx=Template2Parser.Return_or_param_typeContext):
        if ctx.dtype() is not None:
            dtype = self.visit(ctx.dtype())
            return ctx.getText().replace(ctx.dtype().getText(), dtype)
        else:
            return ctx.getText()

    def visitDims(self, ctx=Template2Parser.DimsContext):
        if isinstance(ctx.parentCtx, Template2Parser.Array_accessContext):
            res=""
            for d in ctx.expr():
                if isinstance(d, Template2Parser.NumberContext):
                    res+= str(int(d.getText()) + 1) +","
                else:
                    res+=d.getText() +","
            return res[:-1]
        else:
            return ctx.getText()

    def visitFunction_call(self, ctx):
        func = ctx.FUNCTION().getText()
        
        density_functions = ['bernoulli_logit_lpmf', 'normal_lpdf', 'poisson_log_lpmf', 'binomial_log_lpmf',
                             'bernoulli_log_lpmf', 'binomial_logit_lpmf', 'bernoulli_lpmf', 'bernoulli_lpmf', 'binomial_lpmf']
        if ctx.FUNCTION().getText() in density_functions:
            return '{0}({1} | {2})'.format(func, StanVisitor().visit(ctx.params().param(0)),
                                                           ",".join([StanVisitor().visit(p) for p in
                                                                     ctx.params().param()[1:]]))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        param_str = '('
        try:
            for e in ctx.params().param():
                param_str += self.visit(e) + ','
        except:
            param_str +=" "
        return func + param_str[:-1] + ')'

    def visitVal(self, ctx):
        return ctx.getText()

    def visitVecdivop(self, ctx):
        return self.visit(ctx.expr(0)) + ' ./ ' + self.visit(ctx.expr(1))

    def visitVecmulop(self, ctx):
        return self.visit(ctx.expr(0)) + ' .* ' + self.visit(ctx.expr(1))

    def visitSubset(self, ctx):
        return "{0}[{1}:{2}]".format(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), self.visit(ctx.expr(2)))

    def visitBrackets(self, ctx):
        return '(' + self.visit(ctx.expr()) + ')'

    def visitLeq(self, ctx):
        return self.visit(ctx.expr(0)) + '<=' + self.visit(ctx.expr(1))

    def visitAnd(self, ctx):
        return self.visit(ctx.expr(0)) + "&&" + self.visit(ctx.expr(1))

    def visitEq(self, ctx):
        return self.visit(ctx.expr(0)) + "==" + self.visit(ctx.expr(1))

    def visitGeq(self, ctx):
        return self.visit(ctx.expr(0)) + ">=" + self.visit(ctx.expr(1))

    def visitGt(self, ctx):
        return self.visit(ctx.expr(0)) + ">" + self.visit(ctx.expr(1))

    def visitLt(self, ctx):
        return self.visit(ctx.expr(0)) + "<" + self.visit(ctx.expr(1))

    def visitNe(self, ctx):
        return self.visit(ctx.expr(0)) + "!=" + self.visit(ctx.expr(1))

    def visitArray_access(self, ctx):
        return ctx.ID().getText() + "[" + self.visit(ctx.dims()) + "]"

    def visitUnary(self, ctx):
        return "-"+self.visit(ctx.expr())

    def visitFparam(self, ctx):
        return self.visit(ctx.return_or_param_type())+" " +ctx.ID().getText()

    def visitFparams(self, ctx):
        return ','.join([self.visit(p) for p in ctx.fparam()])

    def visitAddop(self, ctx):
        return self.visit(ctx.expr(0)) + "+" + self.visit(ctx.expr(1))

    def visitMinusop(self, ctx):
        return self.visit(ctx.expr(0)) + "-" + self.visit(ctx.expr(1))

    def visitDivop(self, ctx):
        return self.visit(ctx.expr(0)) + "/" + self.visit(ctx.expr(1))

    def visitMulop(self, ctx):
        lhs = self.visit(ctx.expr(0))
        rhs = self.visit(ctx.expr(1))
        if lhs in self.dtypes and rhs in self.dtypes:
            if self.dtypes[lhs] == 'vector' and self.dtypes[rhs] == 'vector':
                return lhs + " .* " + rhs

        return lhs + "*" + rhs

    def visitExponop(self, ctx):
        return self.visit(ctx.expr(0)) + "^" + self.visit(ctx.expr(1))

    def visitDistexpr(self, ctx):
        args = [self.visit(x) for x in ctx.params().param()]
        exc=['bivariate_poisson_log_lpmf', 'poisbin_lpmf']
        other = ['bivariate_poisson_log']
        arg_str = ''
        for a in args:
            arg_str += str(a) + ","
        if ctx.ID().getText() in exc:
            return '{0}({1} | {2})'.format(ctx.ID().getText(), StanVisitor().visit(ctx.params().param(0)),
                                                           ",".join([StanVisitor().visit(p) for p in
                                                                     ctx.params().param()[1:]]))
        elif ctx.ID().getText() in self.functions or ctx.ID().getText() in other:
            return ctx.ID().getText() + '(' + arg_str[:-1] + ')'
        else:
            dist = [x for x in self.models if x["name"] == ctx.ID().getText()]
            if len(dist) == 0:
                print("Distribution {0} not found".format(ctx.ID().getText()))
                raise Exception
            return dist[0]["stan"] + '(' + arg_str[:-1] + ')'


class StanTranslator(Template2Listener):
    def __init__(self, directory, templatefile, config, old_version=False, isjson=False, datafilename='data.r'):
        self.output_program = ""
        self.data = {}
        self.directory = directory
        self.priors = {}
        self.params_covered = {}
        self.param_decl = ""
        self.param_assigns = ""
        self.models = parse_models()
        self.transformed_params_decl = ""
        self.transformed_params_assign = ""
        self.transformed_data_blk = ""
        self.functions_blk = ""
        self.generatedquantities_blk = ""
        self.modelblk = ""
        self.in_transformed_param = False
        self.curBlock = "model"
        self.dtypes = {}
        self.config = config
        self.templatefile = templatefile
        self.issimplex = []
        self.isold_version = old_version
        self.functions = {}
        self.isjson = isjson
        self.datafilename=datafilename
        

    def run(self, algorithm, timeout, prog_id, python_cmd):
        print("Running Stan program " + str(prog_id) + " >>>>")
        if algorithm == 'nuts':
            process = sp.Popen(
                "cd " + self.directory + "; timeout {0} {1} driver.py sampling 2000".format(timeout, python_cmd),
                stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            dataout, dataerr = process.communicate()

            with open(self.directory + '/stan_nuts_' + str(prog_id), 'w') as outputfile:
                outputfile.write(dataerr)
                outputfile.write(dataout)

        elif algorithm == 'hmc':
            process = sp.Popen(
                "cd " + self.directory + "; timeout {0} {1} driver.py hmc 2000".format(timeout, python_cmd),
                stdout=sp.PIPE, stderr=sp.PIPE, shell=True)

            dataout, dataerr = process.communicate()
            with open(self.directory + '/stan_hmc_' + str(prog_id), 'w') as outputfile:
                outputfile.write(dataerr)
                outputfile.write(dataout)
        elif algorithm == 'vb':
            process = sp.Popen(
                "cd " + self.directory + "; timeout {0} {1} driver.py vb 2000".format(timeout, python_cmd),
                stdout=sp.PIPE, stderr=sp.PIPE, shell=True)

            dataout, dataerr = process.communicate()
            with open(self.directory + '/stan_vb_' + str(prog_id), 'w') as outputfile:
                outputfile.write(dataerr)
                outputfile.write(dataout)

        print("Done Stan program " + str(prog_id) + " >>>>")

    def parseArray(self, array):
        if array.array() is not None and len(array.array()) > 0:
            return np.array([self.parseArray(x) for x in array.array()])
        elif array.vector() is not None and len(array.vector()) > 0:
            return np.array([self.parseVector(x) for x in array.vector()])
        elif array.expr() is not None and len(array.expr()) > 0:
            
            if "." in array.getText():
                return np.array([float(x.getText()) for x in array.expr()])
            else:
                return np.array([int(x.getText()) for x in array.expr()])
        else:
            return np.array([])
            print("Err:" + array.getText())

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
            return np.array([])
            print("Err:" + vector.getText())

    def addToCurBlock(self, content):
        if self.curBlock == 'transformedparam':
            self.transformed_params_assign += content
        elif self.curBlock == 'model':
            self.modelblk += content
        elif self.curBlock == 'transformeddata':
            self.transformed_data_blk += content
        elif self.curBlock == 'generatedquantities':
            self.generatedquantities_blk += content
        elif self.curBlock == 'functions':
            self.functions_blk += content

    def enterData(self, ctx):
        id = ctx.ID().getText()
        print(id)
        if id == 'dummy':
            return
        if ctx.array() is not None:
            arr = self.parseArray(ctx.array())
            self.data[id] = arr
            if ctx.array().vector() is not None and len(ctx.array().vector()) > 0:
                self.dtypes[id] = 'vector'
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
            if ctx.expr().number() is not None:
                self.data[id] = float(ctx.expr().getText()) if ctx.expr().number().DOUBLE() is not None else int(ctx.expr().getText())

    def enterPrior(self, ctx):
        id = ctx.expr().ID().getText()
        dist = ctx.distexpr()
        dims = dist.dims().getText() if dist.dims() is not None else None
        vectordims = dist.vectorDIMS().dims().getText() if dist.vectorDIMS() is not None else None
        limits = ctx.limits().getText() if ctx.limits() is not None else ""
        accessdims = '' if isinstance(ctx.expr(), Template2Parser.RefContext) else '[' + ctx.expr().dims().getText() +']'
        prior = {}
        args = []
        prior["name"] = dist.ID().getText()

        for p in dist.params().param():
            if isinstance(p.expr(), Template2Parser.ValContext):
                args.append(float(p.expr().getText()) if p.expr().number().DOUBLE() is not None else int(p.expr().getText()))
            elif isinstance(p.expr(), Template2Parser.RefContext):
                args.append(p.getText())
            else:
                
                args.append(StanVisitor(self.dtypes).visit(p.expr()))

        if vectordims is not None:
            vectorOrMatrix = 'matrix' if len(dist.vectorDIMS().dims().expr()) > 1 else 'vector'
            self.dtypes[id] = vectorOrMatrix
            if prior["name"] == 'dirichlet' or prior["name"] == 'multinomial':
                vectorOrMatrix = 'simplex'
            elif prior["name"] == 'lkj_corr':
                vectorOrMatrix = 'corr_matrix'
            elif prior["name"] == 'lkj_corr_cholesky':
                vectorOrMatrix = 'cholesky_factor_corr'

            if not self.params_covered.has_key(id):
                if dims is None:
                    self.param_decl += "{3}{0}[{1}] {2};\n".format( limits, vectordims, id, vectorOrMatrix)
                else:
                    self.param_decl += "{4}{0}[{1}] {2}[{3}];\n".format(limits, vectordims, id, dims, vectorOrMatrix)
        else:
            if dims is None:
                self.dtypes[id] = 'arr'
                if not self.params_covered.has_key(id):
                    self.param_decl+="real{1} {0};\n".format(id, limits)
            else:
                if not self.params_covered.has_key(id):
                    self.param_decl+="real{2} {1}[{0}];\n".format(dims, id, limits)
        self.params_covered[id] = True
        
        prior['prior'] = [x for x in self.models if x['name'] == prior["name"]][0]
        args_str = ''
        for arg in args:
                args_str += str(arg) + ","
        
        if not ((prior['prior']['stan'] == 'normal' or prior['prior']['stan'] == 'multinomial' or prior['prior']['stan'] == 'lkj_corr' or prior['prior']['stan'] == 'dirichlet') and ( (len(args) > 0 and str(args[0]) == "1234.0") or (len(args) > 1 and str(args[1]) == "1234.0"))):
            lhs = 'to_vector({0})'.format(id) if vectordims is not None and vectorOrMatrix == 'matrix' and (isinstance(ctx.expr(),Template2Parser.RefContext) or len(ctx.expr().dims().expr()) != 2) else id
            self.modelblk += "{0}{3} ~ {1}({2});\n".format(lhs, prior['prior']['stan'], args_str[:-1], accessdims)

    def enterAssign(self, ctx):
        sv = StanVisitor(self.dtypes, self.functions)
        if ctx.ID() is not None:
            lhs = ctx.ID().getText()
        else:
            if len(ctx.expr()) > 1:
                lhs = sv.visit(ctx.expr(0))
            else:
                lhs = sv.visit(ctx.expr(0))
        if lhs == 'target':
            self.addToCurBlock("{0} += {1};\n".format(lhs, sv.visit(ctx.expr(0)).replace("target","0")))
            return

        if ctx.distexpr() is not None:
            rhs = sv.visit(ctx.distexpr())
        else:
            if len(ctx.expr()) > 1:
                rhs = sv.visit(ctx.expr(1))
            else:
                rhs = sv.visit(ctx.expr(0))
        if self.isold_version:
            self.addToCurBlock("{0} <- {1};\n".format(lhs, rhs))
        else:
            self.addToCurBlock("{0} = {1};\n".format(lhs, rhs))

    def enterTransformeddata(self, ctx):
        self.curBlock = "transformeddata"

    def exitTransformeddata(self, ctx):
        self.curBlock = "model"

    def enterTransformedparam(self, ctx):
        self.curBlock = "transformedparam"

    def exitTransformedparam(self, ctx):
        self.curBlock = "model"

    def enterGeneratedquantities(self, ctx):
        self.curBlock = "generatedquantities"

    def exitGeneratedquantities(self, ctx):
        self.curBlock = "model"

    def enterFunctions(self, ctx):
        self.curBlock = "functions"

    def exitFunctions(self, ctx):
        self.curBlock="model"

    def enterFunction_decl(self, ctx):
        ropt=StanVisitor().visit(ctx.return_or_param_type())
        id=ctx.ID().getText()
        params=StanVisitor().visit(ctx.fparams())
        self.addToCurBlock(ropt+" "+ id + " ("+params+"){\n")
        self.functions[id] = True

    def exitFunction_decl(self, ctx):
        self.addToCurBlock("}\n")

    def enterFor_loop(self, ctx):
        index = ctx.ID().getText()
        start = ctx.expr(0)
        end = ctx.expr(1)
        sv = StanVisitor(self.dtypes)
        self.addToCurBlock("for({0} in {1}:{2}){{\n".format(index,sv.visit(start), sv.visit(end)))

    def enterIf_stmt(self, ctx=Template2Parser.If_stmtContext):
        sv = StanVisitor(self.dtypes)

        self.addToCurBlock("if ({0}){{ \n".format(sv.visit(ctx.expr())))

    def enterElse_blk(self, ctx):
        self.addToCurBlock("\n} \n else {\n")

    def exitIf_stmt(self, ctx):
        self.addToCurBlock("}\n")

    def exitFor_loop(self, ctx):
       self.addToCurBlock("}\n")

    def enterFunction_call(self, ctx):
        if isinstance(ctx.parentCtx, Template2Parser.StatementContext):
            if ctx.FUNCTION().getText() == 'return':
                self.addToCurBlock('return ' + StanVisitor().visit(ctx.params()) + ";\n")
            else:
                self.addToCurBlock(StanVisitor().visit(ctx)+";\n")

    def enterObserve(self, ctx):
        sv = StanVisitor(self.dtypes)
        if len(ctx.expr()) > 1:
            self.addToCurBlock("{0} ~ {1};\n".format(sv.visit(ctx.expr(1)), sv.visit(ctx.expr(0))))
        else:
            self.addToCurBlock("{0} ~ {1};\n".format(sv.visit(ctx.expr(0)), sv.visit(ctx.distexpr())))

    def dumpJson(self, file, content):
        content_sim = {}
        with open(file, "w") as jsonfile:
            for k in six.iterkeys(content):
                if isinstance(content[k], np.ndarray):
                    content_sim[k] = content[k].tolist()
                else:
                    content_sim[k] = content[k]
            jsonfile.write(json.dumps(content_sim))

    def dumpR(self, file, content):

        with open(file, "w") as rfile:
            for k in six.iterkeys(content):
                if isinstance(content[k], np.ndarray):
                    if len(content[k].shape) == 2:
                        nr,nc = content[k].shape
                        rfile.write("".join(
                            [k, " <- ", "structure(c(", ",".join(str(ee) for ee in content[k].flatten(order='C')),
                             "), .Dim=c(", str(nr), ",", str(nc), "))"]))
                    elif len(content[k].shape) == 3:
                        shape = content[k].shape
                        rfile.write("".join([k, " <- ", "structure(c(", ",".join(str(ee) for ee in content[k].flatten(order='C')),
                             "), .Dim=c", str(shape) , ")"]))
                    elif len(content[k].shape) == 1:
                        rfile.write("".join([k, " <- c(", ",".join(str(ee) for ee in content[k]), ")"]))
                    else:
                        print('Unhandled dimension')
                        raise Exception
                else:
                    rfile.write("".join([k, "<-", str(content[k])]))
                rfile.write("\n")

    def enterDecl(self, ctx=Template2Parser.DeclContext):
        code = ""
        for child in ctx.children:
            code+= child.getText() +" "
        if self.curBlock != 'model':
            self.params_covered[ctx.ID().getText()] = True
        self.addToCurBlock(code.replace('float', 'real')+";\n")

    def exitTemplate(self, ctx):
        
        if self.isjson:
            self.dumpJson(self.directory+'/' + self.datafilename, self.data)
        else:
            self.dumpR(self.directory + '/' + self.datafilename, self.data)

        if len(self.functions_blk) > 0:
            self.output_program += "functions{\n"
            self.output_program += self.functions_blk
            self.output_program += "}\n"
        
        if len(self.data.keys())> 0:
            self.output_program += "data{\n"
            for data_key in self.data.keys():
                data_item = self.data[data_key]
                if data_key in self.dtypes and self.dtypes[data_key] == 'matrix':
                    shape = data_item.shape
                    if len(shape) > 2:
                        self.output_program += 'matrix [{0}] {1}[{2}];\n'.format(str(shape[0:2]).replace(',)',
                                                                                                                ')').replace(
                                                                                   '(', '').replace(')', ''), data_key,
                                                                               str(data_item.shape[2:]).replace(',)',
                                                                                                                ')').replace(
                                                                                   '(', '').replace(')', ''))
                    else:
                        self.output_program += 'matrix [{0}] {1};\n'.format(
                            str(data_item.shape).replace(',)', ')').replace('(', '').replace(')', ''),
                            data_key)
                elif data_key in self.dtypes and self.dtypes[data_key] == 'vector':
                    shape = data_item.shape
                    if len(shape) > 1:
                        self.output_program += 'vector [{2}] {1}[{0}];\n'.format(str(shape[0:-1]).replace(',)', ')').replace('(', '').replace(')', ''), data_key, str(data_item.shape[-1]).replace(',)', ')').replace('(', '').replace(')', ''))
                    else:
                        self.output_program += 'vector [{0}] {1};\n'.format(str(data_item.shape).replace(',)',')').replace('(','').replace(')',''),
                                                                         data_key)
                elif isinstance(data_item, np.ndarray):
                    if data_item.dtype == np.int:
                        self.output_program += "int {1}[{0}];\n".format(str(data_item.shape).replace(',)',')').replace('(','').replace(')',''),
                                                                         data_key)
                    else:
                        self.output_program += "real {1}[{0}];\n".format(
                            str(data_item.shape).replace(',)',')').replace('(', '').replace(')', ''),
                            data_key)
                else:
                    if isinstance(data_item, int):
                        self.output_program += "int {0};\n".format(data_key)
                    else:
                        self.output_program += "real {0};\n".format(data_key)
            self.output_program +="}\n"

        if len(self.transformed_data_blk) > 0:
            self.output_program += "transformed data{\n"
            self.output_program += self.transformed_data_blk
            self.output_program += "}\n"

        if len(self.param_decl) > 0:
            
            self.output_program += "parameters {\n"
            self.output_program += self.param_decl
            self.output_program += "}\n"

        if len(self.transformed_params_assign) > 0:
            self.output_program += "transformed parameters{\n"
            self.output_program += self.transformed_params_decl
            self.output_program += self.transformed_params_assign
            self.output_program += "}\n"

        
        self.output_program += "model {\n"
        self.output_program += self.param_assigns
        self.output_program += self.modelblk
        self.output_program += "}\n"

        if len(self.generatedquantities_blk) > 0:
            self.output_program += "generated quantities{\n"
            self.output_program +=self.generatedquantities_blk
            self.output_program += "}\n"



