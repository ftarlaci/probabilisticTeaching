# abstract syntax tree (AST) to represent the structure of the source code

class Tree:
	def _init_(self, rootNode):
		self.rootNode = rootNode
		self.children = []

	def appendChild(self, child):
		self.children.append(child)

	def appendAt(self, child, index):
		self.children.insert(index, child)

	def __str__(self):
		return self.toString(0)

	def toString(self, indent):
		string = '  '
		for i in range(indent):			
			string += self.rootNode + '\n'
		for child in self.children:
			if child:
				string += child.toString(indent + 1)
		return string

	def normalize(self):
		for child in self.children:
			child.normalize()

		if self.rootNode == 'Block':
			newChildren = []

			for child in self.children:
				if child.rootNode == 'Block':
					for grandchild in child.children:
						newChildren.append(grandchild)
				else:
					newChildren.append(child)

			self.children = newChildren

	def makeCode(self):
		return self.makeCodeRecursively(0)

	def makeCodeRecursively(self, indent):
		string = ''
		if self.rootNode != 'Block':
			for i in range(indent):
				string += '  '

		if self.rootNode == 'ForLoop':
			string += 'ForLoop '
			string += self.children[0].rootNode + ':\n'
			string += self.children[1].makeCodeRecursively(indent + 1)

		if self.rootNode == 'Block':
			for child in self.children:
				string += child.makeCodeRecursively(indent)

		if self.rootNode == 'Angle':
			string += 'Angle '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'Comprehension':
			string += 'Comprehension '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'DrawTriangle':
			string += 'DrawTriangle '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'Invariance':
			string += 'Invariance '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'Nesting':
			string += 'Nesting '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'LeftRight':
			string += 'LeftRight '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'SkippedLevelVideo':
			string += 'SkippedLevelVideo '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'Strategy':
			string += 'Strategy '
			string += self.children[0].rootNode + '\n'

		if self.rootNode == 'UsingCounter':
			string += 'UsingCounter '
			string += self.children[0].rootNode + '\n'

		return string

