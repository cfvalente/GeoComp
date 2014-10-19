from geocomp.triangulation.monotone import Above
from geocomp.common.prim import *
from geocomp.triangulation.dcel import *
from geocomp.triangulation.avl import *
from geocomp.triangulation.mergesort import MergeSort

class trapezoid():
	def __init__(self, top, ledge_origin, ledge_destiny, redge_origin, redge_destiny):
		self.top = top
		self.leo = ledge_origin
		self.led = ledge_destiny
		self.reo = redge_origin
		self.red = redge_destiny

	# point > self
	def greater(self, point):
		if(right(self.leo, self.led, point)):
			return 1
		return 0

	# point >= self
	def greaterEqual(self, point):
		if(right_on(self.reo, self.red, point)):
			return 1
		return 0

	# point == self.value
	def equal(self, point):
		if(left_on(self.leo, self.led, point) and right_on(self.reo, self.red, point)):
			return 1 
		return 0

	# n > self
	def greaterN(self, n):
		if(right(n.reo, n.red, self.top)):
			return 1
		return 0
	# n >= self
	def greaterEqualN(self, n):
		if(left_on(n.leo, n.led, self.top)):
			return 1
		return 0
	# n == self
	def equalN(self, n):
		if(left_on(n.leo, n.led, self.top) and right_on(n.reo, n.red, self.top)):
			return 1 
		return 0


def downTip(p, i):
	n = len(p)
	if(Above(p[i], p[(i-1)%n]) and Above(p[i], p[(i+1)%n])):
		return True
	return False

def upTip(p, i):
	n = len(p)
	if(not Above(p[i], p[(i-1)%n]) and not Above(p[i], p[(i+1)%n])):
		return True
	return False


def LeePreparata(p):
	print ""
	n = len(p)
	t = avl()
	d = dcel()
	d.createDCELfromPolygon(p)
	event = MergeSort(p, range(0, n))
	for i in range(0, n):
		if(downTip(p, event[i])):
			print "Caso 2   "+str(event[i])

			node = t.findNode(p[event[i]])
			if(node == None):
				trap = trapezoid(p[event[i]], p[event[i]], p[(event[i]+1)%n], p[event[i]], p[(event[i]-1)%n])
				t.insert(trap)
			else:
				print "Ok"

			#Caso haja trapezio em cima


		elif(upTip(p, event[i])):
			print "Caso 3   "+str(event[i])
		else:
			print "Caso 1   "+str(event[i])
	return 0