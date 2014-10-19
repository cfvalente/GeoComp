

class node():
	def __init__(self, seg):
		self.seg = seg
		self.parent = None
		self.left = None
		self.right = None
		self.height = 1


	def setValue(self, seg):
		self.seg = seg


	def setValueN(self, n):
		self.seg = n.seg


	def greater(self, val):
		if(self.seg < val):
			return 1
		return 0


	def greaterEqual(self, val):
		if(self.seg <= val):
			return 1
		return 0


	def equal(self, val):
		if(self.seg == val):
			return 1
		return 0


	def greaterN(self, n):
		if(self.seg < n.seg):
			return 1
		return 0


	def greaterEqualN(self, n):
		if(self.seg <= n.seg):
			return 1
		return 0


	def equalN(self, n):
		if(self.seg == n.seg):
			return 1
		return 0


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
		if(treeNode.equal(seg)):
			return treeNode
		if(treeNode.greater(seg)):
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


	def rotateRight(self, treeNode):
		L = treeNode.left
		if(treeNode.parent != None):
			if(treeNode.parent.left == treeNode):
				treeNode.parent.left = L
			else:
				treeNode.parent.right = L
		else:
			self.root = L
		L.parent = treeNode.parent
		treeNode.parent = L
		treeNode.left = L.right
		if(treeNode.left != None):
			treeNode.left.parent = treeNode
		L.right = treeNode
		treeNode.height = getHeight(treeNode)
		L.height = getHeight(L)


	def rotateLeft(self, treeNode):
		R = treeNode.right
		if(treeNode.parent != None):
			if(treeNode.parent.left == treeNode):
				treeNode.parent.left = R
			else:
				treeNode.parent.right = R
		else:
			self.root = R
		R.parent = treeNode.parent
		treeNode.parent = R
		treeNode.right = R.left
		if(treeNode.right != None):
			treeNode.right.parent = treeNode
		R.left = treeNode
		treeNode.height = getHeight(treeNode)
		R.height = getHeight(R)

	def balance(self, treeNode):
		lHeight = getHeight(treeNode.left)
		rHeight = getHeight(treeNode.right)

		if(lHeight-rHeight == 2):
			llHeight = getHeight(treeNode.left.left)
			lrHeight = getHeight(treeNode.left.right)
			if(llHeight-lrHeight == -1):
				L = treeNode.left
				self.rotateLeft(L)
			self.rotateRight(treeNode)
		if(lHeight-rHeight == -2):
			rlHeight = getHeight(treeNode.right.left)
			rrHeight = getHeight(treeNode.right.right)
			if(rlHeight-rrHeight == 1):
				R = treeNode.right
				self.rotateRight(R)
			self.rotateLeft(treeNode)
		return


	def insertRec(self, treeNode, newNode):
		#criterio de comparacao, talvez seja necessario alterar
		if(treeNode.greaterN(newNode)):
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
		self.balance(treeNode)


	def insert(self, seg):
		newNode = node(seg)
		if(self.root == None):
			self.root = newNode
		else:
			self.insertRec(self.root,newNode)

	def findSucessorForRemovalRec(self, treeNode):
		if(treeNode.left != None):
			suc = self.findSucessorForRemovalRec(treeNode.left)
		else:
			if(treeNode.parent.left == treeNode):
				treeNode.parent.left = treeNode.right
				if(treeNode.right != None):
					treeNode.right.parent = treeNode.parent
			else:
				treeNode.parent.right = treeNode.right
				if(treeNode.right != None):
					treeNode.right.parent = treeNode.parent
			return treeNode
		treeNode.height = getHeight(treeNode)
		self.balance(treeNode)
		return suc

	def findSucessorForRemoval(self, treeNode):
		suc = self.findSucessorForRemovalRec(treeNode.right)
		return suc


	def removeRec(self, treeNode, seg):
		#busca o node do elemento
		if(treeNode.greater(seg)):
			if(treeNode.right != None):
				self.removeRec(treeNode.right, seg)
			else:
				return 0
		elif(not treeNode.greaterEqual(seg)):
			if(treeNode.left != None):
				self.removeRec(treeNode.left, seg)
			else:
				return 0
		# encontra o node do elemento
		else:
			#node nao tem filhos, eh uma folha - simplesmente apaga e retorna para fazer o rebalanceamento do no acima
			if(treeNode.left == None and treeNode.right == None):
				#node eh a raiz
				if(treeNode.parent == None):
					self.root = None
					return 0
				# node nao eh a raiz
				if(treeNode.parent.left == treeNode):
					treeNode.parent.left = None
					return 0
				else:
					treeNode.parent.right = None
					return 0
			#node nao eh folha, apresenta pelo menos um filho
			else:
				#apresenta apenas o filho esquerdo
				if(treeNode.left != None and treeNode.right == None):
					if(treeNode.parent == None):
						self.root = treeNode.left
						treeNode.left.parent = None
					else:
						if(treeNode.parent.right == treeNode):
							treeNode.parent.right = treeNode.left
							treeNode.left.parent = treeNode.parent
							return 0
						else:
							treeNode.parent.left = treeNode.left
							treeNode.left.parent = treeNode.parent
							return 0
				#apresenta apenas o filho direito
				elif(treeNode.right != None and treeNode.left == None):
					if(treeNode.parent == None):
						self.root = treeNode.right
						treeNode.right.parent = None
					else:
						if(treeNode.parent.right == treeNode):
							treeNode.parent.right = treeNode.right
							treeNode.right.parent = treeNode.parent
							return 0
						else:
							treeNode.parent.left = treeNode.right
							treeNode.right.parent = treeNode.parent
							return 0
				#apresenta 2 filhos
				else:
					suc = self.findSucessorForRemoval(treeNode)
					treeNode.setValueN(suc)

		treeNode.height = getHeight(treeNode)
		self.balance(treeNode)
		return 0


	def remove(self,seg):
		treeNode = self.root
		if not(treeNode == None):
			self.removeRec(treeNode, seg)
		return 1




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
		print("Error!")
		return 0	
	return 1


def balancingTest():
	tree = avl()
	tree.insert(5)
	tree.insert(4)
	tree.insert(3)
	tree.insert(6)
	tree.insert(5.5)
	if not(tree.root.right.seg == 5.5):
		print("Error!");
		return 0
	if not(tree.root.right.left.seg == 5):
		print("Error!");
		return 0
	tree2 = avl()
	for i in range(0,500):
		tree.insert(i)
	for i in range(-10000, -1):
		tree.insert(i)
	
	for i in range(0, 100000):
		tree.insert(i)
# 17 = floor(log2(110500))+1
	if not(tree.root.height == 17):
		print("Error!")
		return 0

	return 1


def removeTest():
	tree = avl()
	tree.remove(42)
	tree.insert(0)
	tree.remove(0)
	tree.insert(0)
	tree.insert(1)
	tree.remove(1)
	tree.insert(1)
	tree.remove(0)
	if not (tree.root.seg == 1):
		print("Error!")
		return 0
	tree2 = avl()
	tree2.insert(4)
	tree2.insert(3)
	tree2.insert(5.5)
	tree2.insert(1)
	tree2.insert(3.5)
	tree2.insert(5)
	tree2.insert(6)
	tree2.insert(7)
	tree2.remove(4)
	if not (tree2.root.seg == 5 and tree2.root.right.seg == 6):
		print("Error!")
		return 0

	tree3 = avl()
	tree3.insert(4)
	tree3.insert(3)
	tree3.insert(5.5)
	tree3.insert(1)
	tree3.insert(3.5)
	tree3.insert(5)
	tree3.insert(6)
	tree3.insert(7)
	tree3.remove(5.5)
	if not (tree3.root.seg == 4 and tree3.root.right.seg == 6 and tree3.root.right.left.seg == 5):
		print("Error!")
		return 0

	tree4 = avl()
	tree4.insert(44)
	tree4.insert(17)
	tree4.insert(78)
	tree4.insert(32)
	tree4.insert(50)
	tree4.insert(88)
	tree4.insert(48)
	tree4.insert(62)
	tree4.remove(32)
	if not(tree4.root.seg == 50):
		print("Error!")
		return 0

	tree5 = avl()
	tree5.insert(50)
	tree5.insert(25)
	tree5.insert(75)
	tree5.insert(10)
	tree5.insert(30)
	tree5.insert(60)
	tree5.insert(80)
	tree5.insert(5)
	tree5.insert(15)
	tree5.insert(27)
	tree5.insert(55)
	tree5.insert(1)
	tree5.remove(80)
	if not(tree5.root.seg == 25):
		print("Error!")
		return 0
	tree6 = avl()
	for i in range(-500, 600):
		tree6.insert(i)
	for i in range(-450, 540):
		tree6.remove(i)
	for i in range(-500, 595):
		tree6.remove(i)
	for i in range(596, 600):
		tree6.remove(i)
	if not(tree6.root.seg == 595):
		print("Error!")
		return 0

	return 1



def test():
	predecessorSucessorTest()
	balancingTest()
	removeTest()