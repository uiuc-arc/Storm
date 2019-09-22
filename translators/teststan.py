#!/usr/bin/env python
import antlr4
from antlr4 import *
from language.antlr.Template2Lexer import Template2Lexer
from language.antlr.Template2Parser import Template2Parser
from language.antlr.Template2Listener import Template2Listener
from newbackends.pyrotranslator import PyroTranslator
from newbackends.stantranslator import StanTranslator
import sys
import os
import argparse
import traceback

parser = argparse.ArgumentParser()
parser.add_argument('-o', default=False, action='store_true') 
parser.add_argument('-j', default=False, action='store_true')
parser.add_argument('program')
args=parser.parse_args()
useoldversion=args.o
isjson = args.j
templatefile=args.program
outputname=templatefile.split("/")[-1].replace(".template","") + ".stan"
if isjson:
    datafilename = templatefile.split("/")[-1].replace(".template", "") + ".json"
else:
    datafilename=templatefile.split("/")[-1].replace(".template","") + ".data.R"


if os.path.exists(outputname):
    os.remove(outputname)

if os.path.exists(datafilename):
    os.remove(datafilename)




template = antlr4.FileStream(templatefile)
lexer = Template2Lexer(template)
stream = antlr4.CommonTokenStream(lexer)
parser = Template2Parser(stream)


try:
    w = StanTranslator('.' ,'.', None, old_version=useoldversion, isjson=isjson, datafilename=datafilename)
    template = parser.template()

    walker = ParseTreeWalker()
    walker.walk(w, template)
    


    with open(outputname, 'w') as output:
        output.write(w.output_program)
except Exception as e:
    print(traceback.format_exc())
    print(e.message)



