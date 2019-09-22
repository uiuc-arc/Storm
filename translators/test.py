#!/usr/bin/env python
import argparse

import antlr4
from antlr4 import *
from language.antlr.Template2Lexer import Template2Lexer
from language.antlr.Template2Parser import Template2Parser
from language.antlr.Template2Listener import Template2Listener
from newbackends.pyrotranslator import PyroTranslator

from language.Reorder import ReOrder

parser = argparse.ArgumentParser()
parser.add_argument('-a')
parser.add_argument('-it', default=4000)
parser.add_argument('-samples', action='store_true')
parser.add_argument('-lr', default=None)
parser.add_argument('-ag', action='store_true')
parser.add_argument('program')
algo=vars(parser.parse_args())['a']
iters=vars(parser.parse_args())['it']
samples=vars(parser.parse_args())['samples']
learning_rate=vars(parser.parse_args())['lr']
templatefile=vars(parser.parse_args())['program']
autoguide=vars(parser.parse_args())['ag']
outputname=templatefile.split("/")[-1].replace(".template","")


class MyWalker(Template2Listener):
    def __init__(self):
        pass

    def enterArith(self, ctx):
        print(ctx)


with open('/tmp/' + outputname , 'w') as tmpfile:
    tmpfile.write(ReOrder(templatefile).reordered_code)
    templatefile='/tmp/' + outputname
template = antlr4.FileStream(templatefile)
lexer = Template2Lexer(template)
stream = antlr4.CommonTokenStream(lexer)
parser = Template2Parser(stream)

w = PyroTranslator(algo, iters,samples, autoguide)

template = parser.template()

walker = ParseTreeWalker()
walker.walk(w, template)


with open(outputname + ".py", 'w') as output:
    output.write(w.output_program)



