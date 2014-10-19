from geocomp.triangulation.monotone import Above
from geocomp.common.prim import *
from geocomp.triangulation.dcel import *
from geocomp.triangulation.avl import *
from geocomp.triangulation.mergesort import MergeSort

class trapezoid():
	def __init__(self, top, topIndex, ledge_origin, ledge_destiny, redge_origin, redge_destiny):
		self.top = top
		self.topIndex = topIndex
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


def downSpike(p, i):
	n = len(p)
	if(Above(p[i], p[(i-1)%n]) and Above(p[i], p[(i+1)%n])):
		return True
	return False

def upSpike(p, i):
	n = len(p)
	if(not Above(p[i], p[(i-1)%n]) and not Above(p[i], p[(i+1)%n])):
		return True
	return False

def orderedDCEL(d, point, n, face):
	edge = d.findEdgeUsingOrigin(point, 1)
	orderedDcel = []
	for i in range(0, n):
		orderedDcel.append(edge)
		edge = edge.next
	return orderedDcel


				
def LeePreparata(p):
	print ""
	n = len(p)
	t = avl()
	d = dcel()
	d.createDCELfromPolygon(p)
	od = orderedDCEL(d, p[0], n, 1)
	event = MergeSort(p, range(0, n))
	IND_FACE = 1
	for i in range(0, n):
		if(downSpike(p, event[i])):
			print "Caso 2   "+str(event[i])

			node = t.findNode(p[event[i]])
			if(node == None):
				trap = trapezoid(p[event[i]], event[i], p[event[i]], p[(event[i]+1)%n], p[event[i]], p[(event[i]-1)%n])
				t.insert(trap)
			else:
				print "Ok"

			#Caso haja trapezio em cima

		# Caso 3 - Ponto para cima
		elif(upSpike(p, event[i])):
			print "Caso 3   "+str(event[i])
			node = t.findNode(p[event[i]])
			suc = t.sucessor(node)
			pred = t.predecessor(node)
			# Caso haja dois trapezios em cima do ponto evento
			if(suc != None and suc.value.equal(p[event[i]])):
				print "Tb esta no trap sucessor"
				trap = trapezoid(p[event[i]], event[i], node.value.leo, node.value.led, suc.value.reo, suc.value.red)
				t.remove(node)
				t.remove(suc)
				t.insert(trap)
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					d.insertEdge(od[event[i]], od[node.value.topIndex], IND_FACE)
				if(downSpike(p, suc.value.topIndex) and abs(event[i]-suc.value.topIndex) > 1):
					d.insertEdge(od[event[i]], od[suc.value.topIndex], IND_FACE)
			elif(pred != None and pred.value.equal(p[event[i]])):
				print "Tb esta no trap predecessor"
				trap = trapezoid(p[event[i]], event[i], pred.value.leo, pred.value.led, node.value.reo, node.value.red)
				t.remove(node)
				t.remove(pred)
				t.insert(trap)
				# Se o ponto do trapezio for ponta pra baixo e nao for adjacente ao ponto evento entao adiciona diagonal
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					d.insertEdge(od[event[i]], od[node.value.topIndex], IND_FACE)
				if(downSpike(p, pred.value.topIndex) and abs(event[i]-pred.value.topIndex) > 1):
					d.insertEdge(od[event[i]], od[pred.value.topIndex], IND_FACE)
			# Caso so haja um trapezio em cima do ponto evento
			else:
				print "So esta em 1 trapezio"
				t.remove(node)
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					d.insertEdge(od[event[i]], od[node.value.topIndex], IND_FACE)

		else:
			print "Caso 1   "+str(event[i])
	return 0