#!/usr/bin/env python
# -*- coding: utf-8 -*-
from geocomp.common.prim import * 
from geocomp.triangulation.dcel import *
from geocomp.triangulation.stack import *
from math import acos
from math import sqrt
from geocomp.triangulation.mergesort import Above
from geocomp.common import control
from geocomp.triangulation.plotpolygon import PlotPolygon


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
	ui.origin.lineto(stt.origin, 'yellow')
	control.sleep ()
	ui.origin.remove_lineto(stt.origin)

	# Parte esquerda do poligono - descrescente
	if((st.origin.y > st.next.origin.y)):
		return right_on(stt.origin, st.origin, ui.origin)
	# Caso degenerado com pontos colineares
	elif(st.origin.y == st.next.origin.y):
		n = st.next
		while(st.origin.y == n.origin.y):
			n = n.next
		if(st.origin.y > n.origin.y):
			return right_on(stt.origin, st.origin, ui.origin)
	# Parte direita do poligono - crescente
	return left_on(stt.origin, st.origin, ui.origin)



def TriangMonotoneUsingDCEL(d):
	for f in range(1, len(d.faces)):
		event = generateDecreasingVerticeList(d, f)
		s = stack()

		s1 = event[0]
		s.insert(event[0])
		s.insert(event[1])
		
		s1.origin.hilight('cyan')

		for i in range(2, len(event)):
			st = s.getTop()
			staux = s.getTop().origin
			staux.hilight('green')
			aux = event[i].origin
			aux.hilight('yellow')
			control.sleep ()

			if(not Adjacent(event[i], s1) and Adjacent(event[i], st)):
				while( s.size > 1 and not Reflex(event[i], st, s.getSecond())):
					s.remove()
					st = s.getTop()
					print(str(event[i].origin)+" "+str(st.origin))
					event[i].origin.lineto(st.origin, 'red')
					control.sleep ()

				s.insert(event[i])
				staux.unhilight()


			elif(Adjacent(event[i], s1) and not Adjacent(event[i], st)):
				while(s.size > 1):
					print(str(event[i].origin)+" "+str(s.getTop().origin))
					event[i].origin.lineto(s.getTop().origin, 'red')
					control.sleep ()
					s.remove()
				s.remove()
				s.insert(st)
				s.insert(event[i])
				s1.origin.unhilight()
				s1 = st
				staux.unhilight()
				control.sleep ()
				s1.origin.hilight('cyan')


			elif(Adjacent(event[i], s1) and Adjacent(event[i], st)):
				s.remove()
				while(s.size > 1):
					print(str(event[i].origin)+" "+str(s.getTop().origin))
					event[i].origin.lineto(s.getTop().origin, 'red')
					control.sleep ()
					s.remove()
				s1.origin.unhilight()
				staux.unhilight()

			else:
				print "wtf"
			aux.unhilight()

			control.sleep ()

	return 0


def Monotone(p):
	print ""
	if(len(p) <= 3):
		return 0
	PlotPolygon(p)
	d = dcel()
	d.createDCELfromPolygon(p)

	TriangMonotoneUsingDCEL(d)

	return 0

