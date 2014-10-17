from geocomp.common.prim import * 
from geocomp.triangulation.dcel import *
from geocomp.triangulation.stack import *
from math import acos
from math import sqrt

# Retorna True caso p esteja acima de q, ou entao caso tenham a mesma y coordenada e p tenha x coordenada menor
def Above(p, q):
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
			print("Are you sure? There are 2 points with the same coordinates."+str(p))
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
			if(Above(l1[ind1].origin, l2[ind2].origin)):
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
			if(Above(e.origin, maxEdge.origin)):
				maxEdge = e
			if(Above(minEdge.origin, e.origin)):
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

def Adjacent(e1, e2):
	if(e1.next.origin == e2.origin or e1.previous.origin == e2.origin):
		return True
	return False


def Angle(p, q, r):
	p.x = 0
	p.y = 0
	q.x = 5
	q.y = 5
	r.x = 5
	r.y = -5


	v1x = q.x-p.x
	v1y = q.y-p.y
	v2x = r.x-p.x
	v2y = r.y-p.y
	n1 = sqrt(v1x*v1x+v1y*v1y)
	n2 = sqrt(v2x*v2x+v2y*v2y)
	v1xn = v1x/n1
	v1yn = v1y/n1
	v2xn = v2x/n2
	v2yn = v2y/n2
	cos = v1xn*v2xn+v1yn*v2yn
	ang = acos(v1xn*v2xn+v1yn*v2yn)

	#ang1 = Angle(Point(0,0), Point(5,5), Point(-5,-5))
	return ang

def Reflex(ui, st, stt):
	#Entao estamos na parte crescente do poligono - parte direita considerando sentido anti horario - com isso basta checar
	if(Above(st.next.origin, st.origin)):
		return left(ui.origin,st.origin,stt.origin)
	#Caso estejamos na parte descrescente temos que checar o inverso
	return right(ui.origin,st.origin,stt.origin)


def TriangMonotoneUsingDCEL(d):
	for f in range(1, len(d.faces)):
		event = generateDecreasingVerticeList(d, f)
		s = stack()

		s1 = event[0]
		s.insert(event[0])
		s.insert(event[1])

		for i in range(2, len(event)):
			st = s.getTop()



			if(not Adjacent(event[i], s1) and Adjacent(event[i], st)):
				#if( s.size > 1 and Angle(st.origin, event[i].origin, s.getSecond().origin) < 3.14159265358979323846):
				while( s.size > 1 and Reflex(event[i], st, s.getSecond())):
					s.remove()
					st = s.getTop()
					print(str(event[i].origin)+" "+str(st.origin))
				s.insert(event[i])



			elif(Adjacent(event[i], s1) and not Adjacent(event[i], st)):
				while(s.size > 1):
					print(str(event[i].origin)+" "+str(s.getTop().origin))
					s.remove()
				s.remove()
				s.insert(st)
				s.insert(event[i])
				s1 = st



			elif(Adjacent(event[i], s1) and Adjacent(event[i], st)):
				s.remove()
				while(s.size > 2):
					print(str(event[i].origin)+" "+str(s.getTop().origin))
					s.remove()

			else:
				print "wtf"


	return 0


def Monotone(p):
	print ""
	d = dcel()
	d.createDCELfromPolygon(p)

	TriangMonotoneUsingDCEL(d)

	return 0