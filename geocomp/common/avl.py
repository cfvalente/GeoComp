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


	def sucessor(self, treeNode):
		if(treeNode == None):
			return None
		if(treeNode.right != None):
			n = treeNode.right
			while(n.left != None):
				n = n.left
			return n
		else:
			n = treeNode
			while(n.parent != None):
				if(n == n.parent.left):
					return n.parent
				n = n.parent
			return None;


	def predecessor(self, treeNode):
		if(treeNode == None):
			return None
		if(treeNode.left != None):
			n = treeNode.left
			while(n.right != None):
				n = n.right
			return n
		else:
			n = treeNode

			while(n.parent != None):
				if(n == n.parent.right):
					return n.parent
				n = n.parent
			return None;


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

def predecessorSucessorTest():
	tree = avl()
	tree.insert(2)
	tree.insert(3)
	tree.insert(-40)
	tree.insert(-60)
	tree.insert(-20)
	tree.insert(-30)
	tree.insert(-10)
	if(not(tree.predecessor(tree.findNode(3)).seg==2)):
		print("Error!")
		return 0
	if(not(tree.sucessor(tree.findNode(3))==None)):
		print("Error!")
		return 0
	if(not(tree.predecessor(tree.findNode(2)).seg==-10)):
		print("Error!")
		return 0
	if(not(tree.sucessor(tree.findNode(2)).seg==3)):
		print("Error!")
		return 0
	if(not(tree.predecessor(tree.findNode(-10)).seg==-20)):
		print("Error!")
		return 0
	if(not(tree.sucessor(tree.findNode(-10)).seg==2)):
		print("Error!")
		return 0
	if(not(tree.predecessor(tree.findNode(-20)).seg==-30)):
		print("Error!")
		return 0
	if(not(tree.sucessor(tree.findNode(-20)).seg==-10)):
		print("Error!")
		return 0
	if(not(tree.predecessor(tree.findNode(-30)).seg==-40)):
		print("Error!")
		return 0
	if(not(tree.sucessor(tree.findNode(-30)).seg==-20)):
		print("Error!")
		return 0
	if(not(tree.predecessor(tree.findNode(-40)).seg==-60)):
		print("Error!")
		return 0
	if(not(tree.sucessor(tree.findNode(-40)).seg==-30)):
		print("Error!")
		return 0
	if(not(tree.predecessor(tree.findNode(-60))==None)):
		print("Error!")
		return 0
	if(not(tree.sucessor(tree.findNode(-60)).seg==-40)):
		print("Erro!")
		return 0	
	return 1


def teste():
	sys.setrecursionlimit(10000)
	if(predecessorSucessorTest()):
		print("Ok")

teste()