#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp.common.prim import * 
from geocomp.triangulation.dcel import *
from geocomp.triangulation.stack import *
from math import acos
from math import sqrt
from geocomp.triangulation.mergesort import Above


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


def Reflex(ui, st, stt):
	#Entao estamos na parte crescente do poligono - parte direita considerando sentido anti horario - com isso basta checar
	if(Above(st.next.origin, st.origin)):
		return not left(ui.origin,st.origin,stt.origin)
	#Caso estejamos na parte descrescente temos que checar o inverso
	return not right(ui.origin,st.origin,stt.origin)


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
				while( s.size > 1 and not Reflex(event[i], st, s.getSecond())):
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
				while(s.size > 1):
					print(str(event[i].origin)+" "+str(s.getTop().origin))
					s.remove()

			else:
				print "wtf"


	return 0


# -- O algoritmo so funciona para poligonos dados no sentido anti horario!!! Em decorrencia do uso da funcao Reflex
def Monotone(p):
	print ""
	d = dcel()
	d.createDCELfromPolygon(p)

	TriangMonotoneUsingDCEL(d)

	return 0



#( 60.0 387.0 ) ( 243.0 395.0 )
#( 60.0 387.0 ) ( 240.0 437.0 )
#( 138.0 357.0 ) ( 243.0 395.0
#( 300.0 347.0 ) ( 138.0 357.0
#( 400.0 307.0 ) ( 138.0 357.0
#( 200.0 285.0 ) ( 400.0 307.0
#( 390.0 237.0 ) ( 200.0 285.0
#( 161.0 204.0 ) ( 390.0 237.0
#( 290.0 197.0 ) ( 161.0 204.0
#( 100.0 174.0 ) ( 290.0 197.0
#( 240.0 137.0 ) ( 100.0 174.0
#( 157.0 95.0 ) ( 364.0 124.0 )
#( 157.0 95.0 ) ( 240.0 137.0 )
#( 224.0 80.0 ) ( 364.0 124.0 )
#( 340.0 67.0 ) ( 224.0 80.0 )
#( 192.0 39.0 ) ( 340.0 67.0 )
#( 312.0 37.0 ) ( 192.0 39.0 )
#( 361.0 12.0 ) ( 192.0 39.0 )