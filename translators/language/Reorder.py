from language.antlr.Template2Parser import Template2Parser
from language.antlr.Template2Lexer import Template2Lexer
from language.antlr.Template2Listener import Template2Listener
from language.antlr.Template2Visitor import Template2Visitor
import antlr4
from antlr4 import TokenStreamRewriter, ParseTreeWalker
from antlr4.IntervalSet import Interval
class UseAnalyzer(Template2Listener):
    def __init__(self):
        self.use = set()
        self.defined = set()
        self.loop = set()

    def enterAssign(self, ctx):

        if ctx.ID() is not None:
            self.defined.add(ctx.ID().getText())
        else:
            self.defined.add(ctx.expr(0).ID().getText())





    def enterPrior(self, ctx):
        self.defined.add(ctx.expr().ID().getText())

    def enterRef(self, ctx):
        id = ctx.ID().getText()
        self.use.add(id)

    def enterFor_loop(self, ctx):
        self.loop.add(ctx.ID().getText())

    def enterArray_access(self, ctx):
        id = ctx.ID().getText()
        self.use.add(id)


class ReOrder(Template2Listener):
    def __init__(self, template_file):
        self.dependency_map = {}
        self.blk = "model"
        self.defined = []
        self.backlog = []
        self.reordered_code = ""
        self.unblocked = False
        template = antlr4.FileStream(template_file)
        lexer = Template2Lexer(template)
        self.stream = antlr4.CommonTokenStream(lexer)
        parser = Template2Parser(self.stream)
        self.rewriter = TokenStreamRewriter.TokenStreamRewriter(self.stream)

        templatenode = parser.template()
        walker = ParseTreeWalker()
        walker.walk(self, templatenode)

    def getList(self, node, getDef=False):
        useAnalyzer = UseAnalyzer()
        walker = ParseTreeWalker()
        walker.walk(useAnalyzer, node)
        if getDef:
            return useAnalyzer.defined
        else:
            return useAnalyzer.use - useAnalyzer.loop - useAnalyzer.defined

    def enterFunctions(self, ctx):
        self.blk="functions"
        self.reordered_code += (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex)))+"\n"

    def exitFunctions(self, ctx):
        self.blk="model"

    def enterTransformeddata(self, ctx):
        self.blk = "transformeddata"
        self.reordered_code+= (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex)))+"\n"

    def enterTransformedparam(self, ctx):
        self.blk = "transformedparam"

        deplist = self.getList(ctx)
        if self.alldefined(deplist):
            self.reordered_code+= (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex)))+"\n"
            defs = self.getList(ctx, True)
            self.defined = self.defined + list(defs)
            self.unblocked = True
        else:
            self.dependency_map[ctx] = deplist
            self.backlog.append(ctx)
            self.unblocked = False


    def exitTransformeddata(self, ctx):
        self.blk = "model"

    def exitTransformedparam(self, ctx):
        self.blk = "model"

    def enterDecl(self, ctx):
        if self.blk == "model":
            self.reordered_code += (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex)))+"\n"

    def alldefined(self, deplist):
        if deplist == None or len(deplist) == 0:
            return True

        for x in deplist:
            if x not in self.defined:
                return False
        return True

    def reassess(self):
        allelements = self.backlog[:]
        unbacklogged = True
        while unbacklogged:
            unbacklogged = False
            for x in self.backlog:
                if self.alldefined(self.dependency_map[x]):
                    self.reordered_code+= (self.stream.getText(Interval(x.start.tokenIndex, x.stop.tokenIndex)))+"\n"
                    if isinstance(x, Template2Parser.PriorContext):
                        self.defined.append(x.expr().ID().getText())
                    elif isinstance(x, Template2Parser.AssignContext):
                        if x.ID() is not None:
                            self.defined.append(x.ID().getText())
                        else:
                            self.defined.append(x.expr(0).ID().getText())
                    if isinstance(x, Template2Parser.TransformedparamContext):
                        self.defined = self.defined + list(self.getList(x, True))
                    self.backlog.remove(x)
                    unbacklogged = True

    def enterData(self, ctx):
        self.reordered_code+= (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex))) +"\n"
        self.defined.append(ctx.ID().getText())

    def enterAssign(self, ctx):
        if self.blk == "model":
            deplist = self.getList(ctx)
            print(ctx.getText())
            print(deplist)
            if self.alldefined(deplist):
                if ctx.ID() is not None:
                    self.defined.append(ctx.ID().getText())
                else:
                    self.defined.append(ctx.expr(0).ID().getText())
                self.reordered_code += (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex))) + "\n"
                self.reassess()
            else:
                self.dependency_map[ctx] = deplist
                self.backlog.append(ctx)
        elif self.blk == "transformeddata" or (self.blk == "transformedparam" and self.unblocked):

            if ctx.ID() is not None:
                self.defined.append(ctx.ID().getText())
            else:
                arr_id = ctx.expr(0).ID().getText()
                if arr_id not in self.defined:
                    self.defined.append(arr_id)


    def enterObserve(self, ctx):
        if self.blk == "model":
            deplist = self.getList(ctx)
            if self.alldefined(deplist):
                self.reordered_code+= (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex)))+"\n"
            else:
                self.dependency_map[ctx] = deplist
                self.backlog.append(ctx)

    def enterIf_stmt(self, ctx):
        deplist = self.getList(ctx)
        if self.alldefined(deplist):
            self.reordered_code +=(self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex))) +"\n"
        else:
            self.dependency_map[ctx] =deplist
            self.backlog.append(ctx)

    def enterFor_loop(self, ctx):
        if self.blk == "model":
            deplist = self.getList(ctx)
            if self.alldefined(deplist):
                defines = self.getList(ctx, True)
                self.defined = self.defined + list(defines)
                self.reordered_code+= (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex))) +"\n"
            else:
                self.dependency_map[ctx] = deplist
                self.backlog.append(ctx)
                self.blk = "loop"

    def exitFor_loop(self, ctx):
        if self.blk == "loop":
            self.blk = "model"

    def enterPrior(self, ctx):
        deplist = self.getList(ctx)

        if self.alldefined(deplist):
            self.reordered_code+= (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex))) +"\n"
            self.defined.append(ctx.expr().ID().getText())
            self.reassess()
        else:
            self.dependency_map[ctx] = deplist
            self.backlog.append(ctx)

    def enterQuery(self, ctx):
        self.reassess()
        self.reordered_code += (self.stream.getText(Interval(ctx.start.tokenIndex, ctx.stop.tokenIndex))) +"\n"


if __name__ == '__main__':
    import sys
    print(ReOrder(sys.argv[1]).reordered_code)
