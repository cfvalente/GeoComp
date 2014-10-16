class snode():


	def __init__(self, value):
		self.value = value
		self.next = None
		self.previous = None


class stack():

	def __init__(self):
		self.top = None
		self.size = 0

	def insert(self, value):
		node = snode(value)
		if(self.size == 0):
			self.top = node
		else:
			self.top.next = node
			node.previous = self.top
			self.top = node
		self.size = self.size+1

	def remove(self):
		if(self.size > 0):
			self.size = self.size-1
			node = self.top 
			self.top = self.top.previous
			return node.value
		return None

	def getTop(self):
		if(self.size > 0):
			return self.top.value
		return None