from geocomp.triangulation.monotone import Above
from geocomp.triangulation.monotone import TriangMonotoneUsingDCEL
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
		if(left(self.reo, self.red, point)):
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



def upSpike(p, i):
	n = len(p)
	if(Above(p[i], p[(i-1)%n]) and Above(p[i], p[(i+1)%n])):
		return True
	return False

def downSpike(p, i):
	n = len(p)
	if(not Above(p[i], p[(i-1)%n]) and not Above(p[i], p[(i+1)%n])):
		return True
	return False

def leftEdge(p, i, n):
	if(left(p[i],p[(i-1)%n], p[(i+1)%n])):
		return -1
	return 1

def downEdge(p, i, n):
	if(Above(p[i], p[(i-1)%n])):
		return -1
	return 1

# Indexando as arestas pelos indices dos vertices - usando origem da aresta como base
def orderedDCEL(d, point, n, face):
	edge = d.findEdgeUsingOrigin(point, 1)
	orderedDcel = []
	list = []
	for i in range(0, n):
		list = []
		list.append(edge)
		orderedDcel.append(list)
		edge = edge.next
	return orderedDcel

def insertEdgeUsingOd(od, d, i, node):
	for j in range(0, len(od[i])):
		for k in range(0, len(od[node.value.topIndex])):
			if(od[node.value.topIndex][k].face == od[i][j].face):
				ne = d.insertEdge(od[i][j], od[node.value.topIndex][k])
				nt = ne.twin
				od[ne.originInd].append(ne)
				od[nt.originInd].append(nt)
				return
	

# Hipotese - Poligono simples e eh dado em sentido anti horario	
def LeePreparata(p):
	print ""
	n = len(p)
	t = avl()
	d = dcel()
	d.createDCELfromPolygon(p)
	od = orderedDCEL(d, p[0], n, 1)
	event = MergeSort(p, range(0, n))


	for i in range(0, n):


		# Caso 2 - Ponta para cima
		if(upSpike(p, event[i])):
			node = t.findNode(p[event[i]])
			# Caso nao haja trapezio em cima de do ponto evento
			if(node == None):
				left = leftEdge(p, event[i], n)
				trap = trapezoid(p[event[i]], event[i], p[event[i]], p[(event[i]+left)%n], p[event[i]], p[(event[i]-left)%n])
				t.insert(trap)
			# Caso haja um trapezio em cima do ponto evento
			else:
				left = leftEdge(p, event[i], n)
				trap1 = trapezoid(p[event[i]], event[i], node.value.leo, node.value.led, p[event[i]], p[(event[i]+left)%n])
				trap2 = trapezoid(p[event[i]], event[i], p[event[i]], p[(event[i]-left)%n], node.value.reo, node.value.red)
				insertEdgeUsingOd(od, d, event[i], node)
				t.remove(node)
				t.insert(trap2)
				t.insert(trap1)
				print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)


		# Caso 3 - Ponta para baixo
		elif(downSpike(p, event[i])):
			node = t.findNode(p[event[i]])
			suc = t.sucessor(node)
			pred = t.predecessor(node)
			# Caso haja dois trapezios em cima do ponto evento
			if(suc != None and suc.value.equal(p[event[i]])):
				trap = trapezoid(p[event[i]], event[i], node.value.leo, node.value.led, suc.value.reo, suc.value.red)
				t.remove(node)
				t.remove(suc)
				t.insert(trap)
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
				if(downSpike(p, suc.value.topIndex) and abs(event[i]-suc.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], suc)
					print str(od[event[i]][0].origin)+str(od[suc.value.topIndex][0].origin)
			elif(pred != None and pred.value.equal(p[event[i]])):
				trap = trapezoid(p[event[i]], event[i], pred.value.leo, pred.value.led, node.value.reo, node.value.red)
				t.remove(node)
				t.remove(pred)
				t.insert(trap)
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
				if(downSpike(p, pred.value.topIndex) and abs(event[i]-pred.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], pred)
					print str(od[event[i]][0].origin)+str(od[pred.value.topIndex][0].origin)

			# Caso so haja um trapezio em cima do ponto evento
			else:
				t.remove(node)
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)

		
		# Caso 1 - Uma aresta para cima e outra para baixo			
		else:
			node = t.findNode(p[event[i]])
			t.remove(node)
			if(collinear(node.value.leo, node.value.led, p[event[i]])):
				trap = trapezoid(p[event[i]], event[i], p[event[i]], p[(event[i]+downEdge(p, event[i], n))%n], node.value.reo, node.value.red)
			else:
				trap = trapezoid(p[event[i]], event[i], node.value.leo, node.value.led, p[event[i]], p[(event[i]+downEdge(p, event[i], n))%n])
			if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
			t.insert(trap)


	#print "\n\n\n"
	#for i in range(0, len(d.faces)):
	#	print "Face "+str(i)
	#	d.printFaceVertices(i)
	#print "\n\n\n"


	TriangMonotoneUsingDCEL(d)
	return 0