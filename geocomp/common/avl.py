import sys

class node():
	def __init__(self, seg):
		self.seg = seg
		self.parent = None
		self.left = None
		self.right = None
		self.height = 1

def getHeight(node):
	l = 0
	r = 0
	if(node == None):
		return 0
	if(node.left != None):
		l = node.left.height
	if(node.right != None):
		r = node.right.height
	return max(r,l)+1


class avl():
	def __init__(self):
		self.root = None


	def findNodeRec(self, treeNode, seg):
		if(treeNode == None):
			return None
		if(seg == treeNode.seg):
			return treeNode
		if(seg > treeNode.seg):
			return self.findNodeRec(treeNode.right, seg)
		else:
			return self.findNodeRec(treeNode.left, seg)

	def findNode(self, seg):
		return self.findNodeRec(self.root, seg)

	def maximum(self):
		treeNode = self.root
		while(treeNode.right != None):
			treeNode = treeNode.right
		return treeNode

	def minimum(self):
		treeNode = self.root
		while(treeNode.left != None):
			treeNode = treeNode.left
		return treeNode

	def insertRec(self, treeNode, newNode):
		#criterio de comparacao, talvez seja necessario alterar
		if(newNode.seg > treeNode.seg):
			if(treeNode.right == None):
				treeNode.right = newNode
				newNode.parent = treeNode
			else:
				self.insertRec(treeNode.right,newNode)	
		else:
			if(treeNode.left == None):
				treeNode.left = newNode
				newNode.parent = treeNode
			else:
				self.insertRec(treeNode.left,newNode)
		treeNode.height = getHeight(treeNode)
		lHeight = getHeight(treeNode.left)
		rHeight = getHeight(treeNode.right)
		#balanceamento
		if((lHeight-rHeight > 1) or (lHeight-rHeight <-1)):
			i = 2


	def insert(self, seg):
		newNode = node(seg)
		if(self.root == None):
			self.root = newNode
		else:
			self.insertRec(self.root,newNode)



def teste():
	sys.setrecursionlimit(10000)
	a = node(1)
	print(getHeight(a.left))
	print(a.height)
	tree = avl()
	tree.insert(2)
	tree.insert(3)
	n = tree.findNode(1)
	n = tree.findNode(2)
	n = tree.findNode(3)
	for i in range(0, 100):
		tree.insert(i)
	n = tree.findNode(4)
	n = tree.maximum()
	n = tree.minimum()
	n = tree.findNode(1002)
	n = tree.findNode(2)

teste()