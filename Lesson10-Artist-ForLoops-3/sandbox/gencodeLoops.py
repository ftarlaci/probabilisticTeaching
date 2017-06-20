import random
import json
from tree import *
import numpy as np
import operator
from htmlGenerator import *
import ast
import codegen

NPROGRAMS = 10000

def main():
	decisionTrees = loadDecisionTrees()
	countMap = {}
	labelMap = {}
	for i in range(NPROGRAMS):
		if i % 10000 == 0:
			print i, len(countMap)
		decisions = set(collectDecisions(decisionTrees))
		tree = generateCode(decisions)
		code = tree.makeCode()
		codeText = str(code)
		countTree(countMap, labelMap, decisions, codeText)
	generateHtml(countMap, labelMap)