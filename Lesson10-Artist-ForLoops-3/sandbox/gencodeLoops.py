#generate code for Lesson 10, Course 3 - Artist 
# Make a predefined tree
# Turn tree into code, print code
# Decisions for course 3
# For 1 set of decisions generate and print code

import random
import json
from tree import *
import numpy as np
import operator
from htmlGenerator import *
import ast

NUMPROGRAMS = 1000000


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


#probability of decisions 
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


#collects decisions from files if "no plan" is not used
def collectDecisions(decisionTrees):
	decisions = []
	for tree in decisionTrees:
		decisions.extend(choose(tree))  
		if 'NoPlan' in decisions:
			return decisions
	return decisions


# Generates the code for the game based on decisions reflected through input files
def generateCode(decisions):
	block = Tree('Block')
	if 'AddColor' in decisions:
		colorBlock = getColor(decisions)
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


#if left/right can be distinguished and there is no confusion, creates the first turn of the player
def generateFirstTurn(decisions):
	left = not 'LeftRightConfusion' in decisions
	andgle = 90
	if 'GetAngles' in decisions:
		angle = 60
		if random.random() < 0.5:
			angle = 20

	if 'Invariance' in decisions:
		left = not left
		angle = 360 - angle

	code = Tree(leftOrRight(left))
	code.addChild(Tree(str(angle)))
	return code


#generates the loop when loop is understood and chosen in the course. 
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


#operates if nesting is not understood by the student
def doesnotGetNesting(decisions):
	if 'DontGetNesting' in decisions:
		if 'GetBody' in decisions:
			return True
	return False


#generates the body and its movement through the body input file. 
def generateBody(decisions):
	if 'GetBody' in decisions:
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


#generates the move reading input in the move.json and appends the child generated to the tree
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


#allows the body turn to be made based on the strategy taken and angle invariance in decisions. 
def generateBodyTurn(decisions):
	left = 'CounterClockwisePlan' in decisions 
	angle = getAngle(decisions)
	if 'LeftRightConfusion' in decisions:
		left = not left
	if 'Angle360Invariance' in decisions:
		left = not leftangle = 360 - angle
	code = Tree(leftOrRight(left))
	code.addChild(Tree(str(angle)))
	return code

# reading the decisions in the strategy.json input file, generates an angle
def getAngle(decisions):
	if 'ThinkTriangle' in decisions:
		return 90
	if 'CounterClockwisePlan' in decisions:
		if 'ThinksToInvertAngle' in decisions:
			return 120
		return 60
	else:
		return 60

def leftOrRight(left):
	if left:
		return 'TurnLeft'
	return 'TurnRight'


#generates random code based on random probability and decisions given
def generateRandomCode(decisions, treeDepth):
	genRandom = random.random()
	prob = 0.7 + depth * 0.3
	if genRandom < prob:
		return generateNode(decisions, treeDepth)
	else:
		code = Tree('Block')
		code.addChild(generateNode(decisions, treeDepth))
		code.addChild(generateNode(decisions, treeDepth + 1))
		return code


# this function generates a random node by making random choises and 
# angles and appends it to the tree 
def generateNode(decisions, treeDepth):
	if random.random() < 0.7:
		if random.random() < 0.5:
			code = Tree('Move')
			load = random.choice([0, 100, 150, 200])
			code.addChild(Tree(str(load)))
			return code
		else:
			left = random.random()
			turnAngle = random.choice(range(0, 45, 180))
			code = Tree(leftOrRight(left))
			code.addChild(Tree(str(angle)))
			return code
	else:
		code = Tree('ForLoop')
		num = random.randomNum(1, 5)
		code.addChild(Tree(str(num)))
		code.addChild(generateRandomCode(decisions, treeDepth + 1))
		return code

	
# by seelcting children, the functions below make the code for the decision tree
def choose(decisionTreeRec):
	decisionTree = []

	if not 'children' in decisionTreeRec:
		return []

	children = decisionTreeRec['children']
	child = pickChild(children)
	decisionTree.append(child['name'])
	decisionTree.extend(choose(child))
	return decisonTree



def pickChild(children)
	bias = []
	for child in children
		bias.append(float(child['weight']))
	prob = np.array(bias) / sum(bias)
	return np.random.choise(children, prob = prob)



if __name__ == '__main__':
	main()


