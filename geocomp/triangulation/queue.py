class qnode():


	def __init__(self, value):
		self.value = value
		self.next = None
		self.previous = None


class queue():

	def __init__(self):
		self.first = None
		self.last = None
		self.size = 0

	def insert(self, value):
		node = qnode(value)
		if(self.size == 0):
			self.first = node
			self.last = node
		else:
			self.last.next = node
			node.previous = self.last
			self.last = node
		self.size = self.size+1

	def remove(self):
		if(self.size > 0):
			self.size = self.size-1
			node = self.first 
			self.first = self.first.next
			return node.value
		return None

	def getLast(self):
		if(self.size > 0):
			return self.last.value
		return None