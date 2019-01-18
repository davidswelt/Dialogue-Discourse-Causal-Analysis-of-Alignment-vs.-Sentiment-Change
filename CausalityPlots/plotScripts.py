'''
Created on Nov 16, 2016

@author: ywang
'''
import codecs
import pymysql
import sys
import time
import collections
import numpy
import statsmodels.stats.weightstats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sympy
import matplotlib
import re
import os
import numpy as np
import csv

def setHatchThickness(value):
    libpath = matplotlib.__path__[0]
    backend_pdf = libpath + "/backends/backend_pdf.py"
    with open(backend_pdf, "r") as r:
        code = r.read()
        code = re.sub(r'self\.output\((\d+\.\d+|\d+)\,\ Op\.setlinewidth\)',
                   "self.output(%s, Op.setlinewidth)" % str(value), code)
        with open('/tmp/hatch.tmp', "w") as w:
            w.write(code)
        print backend_pdf
        os.system('sudo mv /tmp/hatch.tmp %s' % backend_pdf)


def plotLexEm(PosFEst,cLexThresList,vline,height,fileName):
    pp = PdfPages(fileName)
    fig = plt.figure()
    markerdic={}

    markerdic['posaposr']='e(+A(LEX)^+r, +f)'
    markerdic['negaposr']='e(-A(LEX)^+r, +f)'
    markerdic['posanegr']='e(+A(LEX)^-r, -f)'
    markerdic['neganegr']='e(-A(LEX)^-r, -f)'

    markers=['o', '^', 'x', 's', '*', 'p', 'h', 'H', 'D', 'd', '<', '>' ]
    patterns = ['-', '+', 'x', '\\', '*', 'o', 'O', '.']
    markersty=0
    
    print PosFEst
    print cLexThresList
    for i in PosFEst:        
        Line=plt.plot(cLexThresList,PosFEst[i],label=markerdic[i])
        plt.setp(Line, marker=markers[markersty], color='black')
        markersty+=1
        
    plt.xlabel('Linguistic Alignment Threshold', fontsize=16)
    plt.ylabel('Causal Significance', fontsize=16)
    plt.ylim(0,height)
    plt.vlines(vline,0,height)
    leg=plt.legend(bbox_to_anchor=(0.99, 0.99), loc=1, borderaxespad=0.,fontsize='large')
#     leg=plt.legend(bbox_to_anchor=(0.01, 0.01), loc=3 , borderaxespad=0.,fontsize='small')
#     leg=plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2 , borderaxespad=0.,fontsize='small')
    leg.get_frame().set_linewidth(0.0)
    setHatchThickness(0.5)
    pp.savefig(fig,dpi=300)
    pp.close()


def plotSynEm(PosFEst,cLexThresList,vline,height,fileName):
    pp = PdfPages(fileName)
    fig = plt.figure()
    markerdic={}

    markerdic['posaposr']='e(+A(SYN)^+r, +f)'
    markerdic['negaposr']='e(-A(SYN)^+r, +f)'
    markerdic['posanegr']='e(+A(SYN)^-r, -f)'
    markerdic['neganegr']='e(-A(SYN)^-r, -f)'

    markers=['o', '^', 'x', 's', '*', 'p', 'h', 'H', 'D', 'd', '<', '>' ]
    patterns = ['-', '+', 'x', '\\', '*', 'o', 'O', '.']
    markersty=0
    
    print PosFEst
    print cLexThresList
    for i in PosFEst:        
        Line=plt.plot(cLexThresList,PosFEst[i],label=markerdic[i])
        plt.setp(Line, marker=markers[markersty], color='black')
        markersty+=1
        
    plt.xlabel('Linguistic Alignment Threshold', fontsize=16)
    plt.ylabel('Causal Significance', fontsize=16)
    plt.ylim(0,height)
    plt.vlines(vline,0,height)
    leg=plt.legend(bbox_to_anchor=(0.99, 0.99), loc=1, borderaxespad=0.,fontsize='large')
#     leg=plt.legend(bbox_to_anchor=(0.01, 0.01), loc=3 , borderaxespad=0.,fontsize='small')
#     leg=plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2 , borderaxespad=0.,fontsize='small')
    leg.get_frame().set_linewidth(0.0)
    setHatchThickness(0.5)
    pp.savefig(fig,dpi=300)
    pp.close()


if __name__ == '__main__':
	reader = csv.reader(open('./data/PosF_Lex.csv', 'r'))
	posFLex = {}
	for row in reader:
   		key = row[0]
   		value = row[1:]
   		posFLex[key] = value
	cLexThresList = posFLex.pop('threshold', None)
	plotLexEm(posFLex,cLexThresList,0.00255,0.08,"./plot/2019posF05Lex20.pdf")

	reader = csv.reader(open('./data/NegF_Lex.csv', 'r'))
	negFLex = {}
	for row in reader:
   		key = row[0]
   		value = row[1:]
   		negFLex[key] = value
	cLexThresList = negFLex.pop('threshold', None)
	plotLexEm(negFLex,cLexThresList,0.00255,0.20,"./plot/2019negF05Lex20.pdf")

	reader = csv.reader(open('./data/PosF_Syn.csv', 'r'))
	posFSyn = {}
	for row in reader:
   		key = row[0]
   		value = row[1:]
   		posFSyn[key] = value
	cSynThresList = posFSyn.pop('threshold', None)
	plotLexEm(posFSyn,cSynThresList,0.00585,0.10,"./plot/2019posF05Syn20.pdf")

	reader = csv.reader(open('./data/NegF_Syn.csv', 'r'))
	negFSyn = {}
	for row in reader:
   		key = row[0]
   		value = row[1:]
   		negFSyn[key] = value
	cSynThresList = negFSyn.pop('threshold', None)
	plotLexEm(negFSyn,cSynThresList,0.00585,0.30,"./plot/2019negF05Syn20.pdf")
