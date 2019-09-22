#!/usr/bin/env python
import antlr4
from antlr4 import *
from language.antlr.Template2Lexer import Template2Lexer
from language.antlr.Template2Parser import Template2Parser
from language.antlr.Template2Listener import Template2Listener
from newbackends.pyrotranslator021 import PyroTranslator
from newbackends.stantranslator import  StanTranslator
import sys
import argparse
from language.Reorder import ReOrder
import os
parser = argparse.ArgumentParser()
parser.add_argument('-a')
parser.add_argument('-i', default=False, action='store_true')
parser.add_argument('-bt', default=False, action='store_true')
parser.add_argument('-it', default=4000)
parser.add_argument('-reorder', default=True, action='store_true')
parser.add_argument('program')
algo=vars(parser.parse_args())['a']
betas=vars(parser.parse_args())['bt']
post=vars(parser.parse_args())['i']
iters=vars(parser.parse_args())['it']
reorder=vars(parser.parse_args())['reorder']
templatefile=vars(parser.parse_args())['program']
outputname=templatefile.split("/")[-1].replace(".template","") + ".py"
if os.path.exists('ss2.py'):
    os.remove('ss2.py')













if reorder:
    with open('/tmp/ss.template', 'w') as tmpfile:
        tmpfile.write(ReOrder(templatefile).reordered_code)
        templatefile='/tmp/ss.template'
template = antlr4.FileStream(templatefile)
lexer = Template2Lexer(template)
stream = antlr4.CommonTokenStream(lexer)
parser = Template2Parser(stream)

w = PyroTranslator(algo,post, betas, iters)

template = parser.template()

walker = ParseTreeWalker()
walker.walk(w, template)


with open(outputname, 'w') as output:
    output.write(w.output_program)



