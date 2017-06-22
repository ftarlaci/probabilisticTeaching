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


#walks the tree to see if there is anything in it; if so, adds them to the countmap and labelmap
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

def generateCode(decisions):
	block = Tree('Block')
	if 'AddColor' in decisions:
		colorBlocj = getColor(decisions)
		block.addChild(colorBlock)
	if 'ClockwisePlan' in decisions:
		if 'ClockwiseTurn' in decisions:
			block.addChild(generateFirstTurn(decisions))
		block.addChild(generateLoop(decisions))
	if 'CounterClockwisePlan' in decisions:
		block.addChild(generateLoop(decisions))
	if 'NoPlan' in decisions:
		block = generateRandomCode(decisions, 0)
	block.normalize()
	return block

def getColor(decisions):
	block = Tree('Color')
	if 'AddRandomColor' in decisions:
		block.addChild(Tree('Red'))
	else:
		block.addChild(Tree('Random'))
	return block

def generateFirstTurn(decisions):
	left = not 'LeftRightConfusion' in decisions
	andgle = 90
	if 'GetAngles' in decisions:
		angle = 60
		if random.random() < 0.5:
			angle = 30

	if 'Invariance' in decisions:
		left = not left
		angle = 360 - angle

	code = Tree(getTurnString(left))
	code.addChild(Tree(str(angle)))
	return code

def generateLoop(decisions):
	if 'GetLoop' in decisions:
		num = getLoopN(decisions)
		loop = Tree('ForLoop')
		loop.addChild(Tree(str(num)))
		loop.addChild(generateBody(decisions))
		if doesnotGetNesting(decisions):
			repeatBody = loop.children[1]
			assert len(repeatBody.children) == 2

			newBlock = Tree('Block')
			newBlock.addChild(loop)
			newBlock.addChild(repeatBody.children[1])
			loop.children[1] = repeatBody.children[0]
			return newBlock
		else:
			return loop
	else:
		code = Tree('Block')
		numBodies = getBodyNum(decisions)
		bodyCode = generateBody(decisions)
		for i in range(numBodies):
			code.addChild(bodyCode)
		return code

def doesnotGetNesting(decisions):
	if 'DontGetNesting' in decisions:
		if 'GetBody' in decisions:
			return True
	return False

def generateBody(decisions):
	if 'GetBody' ind decisions:
		body = Tree('Block')
		if 'GetBodyOrder' in decisions:
			body.addChild(generateMove(decisions))
			body.addChild(generateBodyTurn(decisions))
		else:
			body.addChild(generateBodyTurn(decisions))
			body.addChild(generateMove(decisions))
		return body
	if 'OneBlockBody' in decisions:
		if random.random() < 0.5:
			return generateMove(decisions)
		else:
			return generateBodyTurn(decisions)
	if 'BodyConfusion' in decisions:
		return generateRandomCode(decisions, 0)

def generateMove(decisions):
	code = Tree('Move')
	if 'Move60' in decisions:
		code.addChild(Tree(str(60)))
	else:
		code.addChild(Tree(str(90)))
	return code

def getBodyNum(decisions):
	if 'NoRepeat' in decisions:
		return 1
	if 'GetSideCount' in decisions:
		return 3
	return random.choice([2, 4])

def getLoopN(decisions):
	if 'GetSideCount' in decisions:
		return 3
	if 'DontGetSideCount' in decisions:
		return random.choice([1, 2, 4])

def generateBodyTurn(decisions):
	left = 'CounterClockwisePlan' in decisions 
	angle = getAngle(decisions)
	if 'LeftRightConfusion' in decisions:
		left = not left
	if 'Angle360Invariance' in decisions:
		left = not leftangle = 360 - angle
	code = TRee(getTurnString(left))
	code.addChild(Tree(str(angle)))
	return code

def getAngle(decisions):
	if 'ThinkTriangle' in decisions:
		return 90
	if 'CounterClockwisePlan' in decisions:
		if 'ThinksToInvertAngle' in decisions:
			return 120
		return 60
	else:
		return 60

def getTurnString(left):
	if left:
		return 'TurnLeft'
	return 'TurnRight'

def generateRandomCode(decisions, treeDepth)
	
#TODO make decisions,  generateRandomCode()

