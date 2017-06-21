# abstract syntax tree (AST) to represent the structure of the source code

class tree.AST:
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
