from geocomp.common.prim import * 
from geocomp.triangulation.dcel import *
from geocomp.triangulation.stack import *

# Retorna True caso p esteja acima de q, ou entao caso tenham a mesma y coordenada e p tenha x coordenada menor
def above(p, q):
	if(p.y > q.y):
		return True
	elif(p.y < q.y):
		return False
	else:
		if(p.x < q.x):
			return True
		elif(p.x > q.x):
			return False
		else:
			print("Equal vertices? Is this allowed Arnaldo?")
			return True

# Merge assumindo listas decrescentes
def Merge(l1, l2):
	len1 = len(l1)
	len2 = len(l2)
	res = []
	ind1 = 0
	ind2 = 0
	for i in range(0, len1+len2):
		if(ind1 < len1 and ind2 < len2):
			if(above(l1[ind1].origin, l2[ind2].origin)):
				res.append(l1[ind1])
				ind1 = ind1+1
			else:
				res.append(l2[ind2])
				ind2 = ind2+1
		elif(ind1 < len1 and ind2 == len2):
			res.append(l1[ind1])
			ind1 = ind1+1
		else:
			res.append(l2[ind2])
			ind2 = ind2+1
	return res


def generateDecreasingVerticeList(dcel, face):
	l1 = []
	l2 = []
	res = []
	minEdge = dcel.faces[face]
	maxEdge = dcel.faces[face]
	origin = dcel.faces[face].origin

	e = dcel.faces[face].next
	while(e.origin != origin):
			if(above(e.origin, maxEdge.origin)):
				maxEdge = e
			if(above(minEdge.origin, e.origin)):
				minEdge = e
			e = e.next

	e = maxEdge
	while(e.origin != minEdge.origin):
		l1.append(e)
		e = e.next
	l1.append(minEdge)

	e = maxEdge.previous
	while(e.origin != minEdge.origin):
		l2.append(e)
		e = e.previous

	return Merge(l1,l2)

def adjacent(e1, e2):
	if(e1.next.origin == e2.origin or e1.previous.origin == e2.origin):
		return True
	return False

def Monotone(p):
	print ""
	d = dcel()
	d.createDCELfromPolygon(p)
	#d.printFaceVertices(1)

	for f in range(1, len(d.faces)):
		event = generateDecreasingVerticeList(d, f)
		s = stack()

		s1 = event[0]
		s.insert(event[0])
		s.insert(event[1])

		for i in range(2, len(event)):
			
			if(not adjacent(event[i], s1) and adjacent(event[i], s.getTop())):
				print "caso a"
			elif(adjacent(event[i], s1) and not adjacent(event[i], s.getTop())):
				print "caso b"
			elif(adjacent(event[i], s1) and adjacent(event[i], s.getTop())):
				print "caso c"
			else:
				print "merda"

	#print(len(d.faces))

	return 0