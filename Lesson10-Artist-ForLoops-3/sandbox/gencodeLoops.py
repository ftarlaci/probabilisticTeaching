#generate code for Lesson 10, Course 3 - Artist 

import random
import json
from tree import *
import numpy as np
import operator
from htmlGenerator import *
import ast

NUMPROGRAMS = 10000


#load the decision trees and generate code based on random decisions. 
def main():
	decisionTrees = loadDecisionTrees()
	countMap = {}
	labelMap = {}
	for i in range(NUMPROGRAMS):
		if i % 10000 == 0:
			print i, len(countMap)
		decisions = set(collectDecisions(decisionTrees))
		tree = generateCode(decisions)
		code = tree.makeCode()
		codeText = str(code)
		countTree(countMap, labelMap, decisions, codeText)





# load decision .json files as input 
def loadDecisionTrees():
	trees = []
	treeNames = json.load(open('input/decisions.json'))
	for name in treeNames:
		filePath = 'input/' + name + '.json'
		tree = json.load(open(filePath))
		trees.append(tree)
	return trees	