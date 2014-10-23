#!/usr/bin/env python
# -*- coding: utf-8 -*-
class node():
	def __init__(self, value):
		self.value = value
		self.parent = None
		self.left = None
		self.right = None
		self.height = 1


	def setValue(self, value):
		self.value = value


	def setValueN(self, n):
		self.value = n.value


	def greater(self, val):
		return self.value.greater(val)

	def equal(self, val):
		return self.value.equal(val)

	def greaterN(self, n):
		return self.value.greaterN(n)

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


	def findNodeRec(self, treeNode, value):
		if(treeNode == None):
			return None
		if(treeNode.equal(value)):
			return treeNode
		if(treeNode.greater(value)):
			return self.findNodeRec(treeNode.right, value)
		else:
			return self.findNodeRec(treeNode.left, value)


	def findNode(self, value):
		return self.findNodeRec(self.root, value)


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


	# Faz o balanceamento da arvore - diferenca em altura das duas subarvores de cada no nao pode ser maior que 2
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
		if(treeNode.greaterN(newNode.value)):
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

	# Insere um trapezio na arvore
	def insert(self, value):
		newNode = node(value)
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

	def removeRec(self, treeNode, node):
		#busca o node do elemento
		if(treeNode == node):
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

		elif(treeNode.greaterN(node.value)):
			if(treeNode.right != None):
				self.removeRec(treeNode.right, node)
			else:
				return 0
		else:
			if(treeNode.left != None):
				self.removeRec(treeNode.left, node)
			else:
				return 0

		treeNode.height = getHeight(treeNode)
		self.balance(treeNode)
		return 0

	# Remove o trapezio dado em value da arvore
	def remove(self,node):
		treeNode = self.root
		if not(treeNode == None):
			self.removeRec(treeNode, node)
		return 1
