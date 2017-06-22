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


#walks the tree to see fif there is anything in it; if so, adds them to the countmap and labelmap
def countTree(countMap, labelMap, decisions, tree):
	decisionstring = getDecisionString(decisions)
	treeString = str(tree)
	if not treeString in countMap:
		countMap[treeString] = 0
	countMap[treeString] += 1
	if not treeString in labelMap:
		labelMap[treeString] = {}
	if not decisionstring in labelMap[treeString]:
		labelMap[treeString][decisionstring] = 0
	labelMap[treeString][decisionstring] += 1


# load decision .json files as input 
def loadDecisionTrees():
	trees = []
	treeNames = json.load(open('input/decisions.json'))
	for name in treeNames:
		filePath = 'input/' + name + '.json'
		tree = json.load(open(filePath))
		trees.append(tree)
	return trees	


def labelProbability(labelMap, treeString, count):
	decisionCount = {}
	decisions = labelMap[treeString]
	for decisionSet in decisions:
		for eachDecision in decisionSet:
			if not eachDecision in decisionCount:
				decisionCount[eachDecision] = 0.0
			decisionCount[eachDecision] += 1
	for key in decisionCount:
		decisionCount[key] /= count
	return decisionCount

def decisionString(decisions):
	decisionList = list(decisions)
	decisionList.sort()
	decisionString = ''
	for eachDecision in decisionList:
		decisionString += eachDecision + '\n'
	return decisionString

def collectDecisions(decisionTrees):
	decisions = []
	for tree in decisionTrees:
		decisions.extend(choose(tree))  #chose in collectDecisions
		if 'NoPlan' in decisions
	return decisions

# GENERATE CODE 

