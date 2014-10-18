from geocomp.triangulation.monotone import Above
from geocomp.common.prim import *
from geocomp.triangulation.dcel import *
from geocomp.triangulation.avl import *
from geocomp.triangulation.mergesort import MergeSort

class tetrahedron():
	def __init__(self, top, ledge_origin, ledge_destiny, redge_origin, redge_destiny):
		self.top = top
		self.leo = ledge_origin
		self.led = ledge_destiny
		self.reo = redge_origin
		self.red = redge_destiny



	def insideTetrahedron(self, point):
		return self.equal(point)

	def greater(self, point):
		if(left(self.leo, self.led, point) and left(self.reo, self.red, point)):
			return 1
		return 0


	def greaterEqual(self, point):
		if(left_on(self.leo, self.led, point)):
			return 1
		return 0


	def equal(self, point):
		if(left_on(self.leo, self.led, point) and right_on(self.reo, self.red, point)):
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
	t = avl()
	d = dcel()
	d.createDCELfromPolygon(p)
	event = MergeSort(p, range(0, len(p)))
	for i in range(0, len(event)):
		if(downTip(p, event[i])):
			print "Caso 2   "+str(event[i])
		elif(upTip(p, event[i])):
			print "Caso 3   "+str(event[i])
		else:
			print "Caso 1   "+str(event[i])
	return 0