#!/usr/bin/env python
# -*- coding: utf-8 -*-
from geocomp.triangulation.monotone import Above
from geocomp.triangulation.monotone import TriangMonotoneUsingDCEL
from geocomp.common.prim import *
from geocomp.triangulation.dcel import *
from geocomp.triangulation.avl import *
from geocomp.triangulation.mergesort import MergeSort
from geocomp.common import control
from geocomp.triangulation.plotpolygon import PlotPolygon

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
		if(left_on(self.reo, self.red, n.top) and left_on(self.reo, self.red, n.top)):
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
def orderedDCEL(d, point, n):
	edge = d.findEdgeUsingOrigin(point, 1)
	orderedDcel = []
	list = []
	for i in range(0, n):
		list = []
		list.append(edge)
		orderedDcel.append(list)
		edge = edge.next
	return orderedDcel

def inCone(od, edge1, edge2):
	u = edge1.previous
	w = edge1.next
	if(left_on(u.origin, edge1.origin, w.origin)):
		return (left(edge1.origin, edge2.origin, u.origin) and left(edge2.origin, edge1.origin, w.origin))
	return not ( left_on(edge1.origin, edge2.origin, w.origin) and left_on(edge2.origin, edge1.origin, u.origin) )


def insertEdgeUsingOd(od, d, i, node):
	for j in range(0, len(od[i])):
		for k in range(0, len(od[node.value.topIndex])):
			if(inCone(od, od[i][j], od[node.value.topIndex][k]) and inCone(od, od[node.value.topIndex][k], od[i][j])):
				ne = d.insertEdge(od[i][j], od[node.value.topIndex][k])
				nt = ne.twin
				od[ne.originInd].append(ne)
				od[nt.originInd].append(nt)
				return
	

def LeePreparata(p):
	print ""
	if(len(p) <= 3):
		return 0
	PlotPolygon(p)
	n = len(p)
	t = avl()
	d = dcel()
	d.createDCELfromPolygon(p)
	od = orderedDCEL(d, p[0], n)
	event = MergeSort(p, range(0, n))


	for i in range(0, n):


		p[event[i]].hilight('yellow')

		# Caso 2 - Ponta para cima
		if(upSpike(p, event[i])):
			node = t.findNode(p[event[i]])
			# Caso nao haja trapezio em cima de do ponto evento
			if(node == None):
				left = leftEdge(p, event[i], n)
				trap = trapezoid(p[event[i]], event[i], p[event[i]], p[(event[i]+left)%n], p[event[i]], p[(event[i]-left)%n])
				t.insert(trap)
				control.sleep ()
			# Caso haja um trapezio em cima do ponto evento
			else:
				node.value.leo.lineto(node.value.led, 'green')
				node.value.reo.lineto(node.value.red, 'green')
				node.value.top.hilight('green')
				control.sleep ()
				left = leftEdge(p, event[i], n)
				trap1 = trapezoid(p[event[i]], event[i], node.value.leo, node.value.led, p[event[i]], p[(event[i]+left)%n])
				trap2 = trapezoid(p[event[i]], event[i], p[event[i]], p[(event[i]-left)%n], node.value.reo, node.value.red)
				insertEdgeUsingOd(od, d, event[i], node)
				print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
				od[event[i]][0].origin.lineto(od[node.value.topIndex][0].origin, 'red')
				control.sleep ()
				node.value.leo.remove_lineto(node.value.led)
				node.value.reo.remove_lineto(node.value.red)
				node.value.top.unhilight()
				t.remove(p[event[i]])
				t.insert(trap2)
				t.insert(trap1)


		# Caso 3 - Ponta para baixo
		elif(downSpike(p, event[i])):
			node = t.findNode(p[event[i]])
			suc = t.sucessor(node)
			pred = t.predecessor(node)
			node.value.leo.lineto(node.value.led, 'green')
			node.value.reo.lineto(node.value.red, 'green')
			node.value.top.hilight('green')
			# Caso haja dois trapezios em cima do ponto evento
			if(suc != None and suc.value.equal(p[event[i]])):
				suc.value.leo.lineto(suc.value.led, 'cyan')
				suc.value.reo.lineto(suc.value.red, 'cyan')
				suc.value.top.hilight('cyan')
				control.sleep ()
				trap = trapezoid(p[event[i]], event[i], node.value.leo, node.value.led, suc.value.reo, suc.value.red)
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
					od[event[i]][0].origin.lineto(od[node.value.topIndex][0].origin, 'red')
				if(downSpike(p, suc.value.topIndex) and abs(event[i]-suc.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], suc)
					print str(od[event[i]][0].origin)+str(od[suc.value.topIndex][0].origin)	
					od[event[i]][0].origin.lineto(od[suc.value.topIndex][0].origin, 'red')
				control.sleep ()
				node.value.leo.remove_lineto(node.value.led)
				node.value.reo.remove_lineto(node.value.red)
				node.value.top.unhilight()
				suc.value.leo.remove_lineto(suc.value.led)
				suc.value.reo.remove_lineto(suc.value.red)
				suc.value.top.unhilight()
				t.remove(p[event[i]])
				t.remove(p[event[i]])
				t.insert(trap)
				control.sleep ()
			elif(pred != None and pred.value.equal(p[event[i]])):
				pred.value.leo.lineto(pred.value.led, 'cyan')
				pred.value.reo.lineto(pred.value.red, 'cyan')
				pred.value.top.hilight('cyan')
				control.sleep ()
				trap = trapezoid(p[event[i]], event[i], pred.value.leo, pred.value.led, node.value.reo, node.value.red)
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
					od[event[i]][0].origin.lineto(od[node.value.topIndex][0].origin, 'red')
				if(downSpike(p, pred.value.topIndex) and abs(event[i]-pred.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], pred)
					print str(od[event[i]][0].origin)+str(od[pred.value.topIndex][0].origin)
					od[event[i]][0].origin.lineto(od[pred.value.topIndex][0].origin, 'red')
				control.sleep ()
				node.value.leo.remove_lineto(node.value.led)
				node.value.reo.remove_lineto(node.value.red)
				node.value.top.unhilight()
				pred.value.leo.remove_lineto(pred.value.led)
				pred.value.reo.remove_lineto(pred.value.red)
				pred.value.top.unhilight()
				t.remove(p[event[i]])
				t.remove(p[event[i]])
				t.insert(trap)
				control.sleep ()

			# Caso so haja um trapezio em cima do ponto evento
			else:
				if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
					od[event[i]][0].origin.lineto(od[node.value.topIndex][0].origin, 'red')
				control.sleep ()
				node.value.leo.remove_lineto(node.value.led)
				node.value.reo.remove_lineto(node.value.red)
				node.value.top.unhilight()
				t.remove(p[event[i]])
				control.sleep ()

		
		# Caso 1 - Uma aresta para cima e outra para baixo			
		else:
			node = t.findNode(p[event[i]])
			node.value.leo.lineto(node.value.led, 'green')
			node.value.reo.lineto(node.value.red, 'green')
			node.value.top.hilight('green')
			if(collinear(node.value.leo, node.value.led, p[event[i]])):
				trap = trapezoid(p[event[i]], event[i], p[event[i]], p[(event[i]+downEdge(p, event[i], n))%n], node.value.reo, node.value.red)
			else:
				trap = trapezoid(p[event[i]], event[i], node.value.leo, node.value.led, p[event[i]], p[(event[i]+downEdge(p, event[i], n))%n])
			if(downSpike(p, node.value.topIndex) and abs(event[i]-node.value.topIndex) > 1):
					insertEdgeUsingOd(od, d, event[i], node)
					print str(od[event[i]][0].origin)+str(od[node.value.topIndex][0].origin)
					od[event[i]][0].origin.lineto(od[node.value.topIndex][0].origin, 'red')
			control.sleep ()
			node.value.leo.remove_lineto(node.value.led)
			node.value.reo.remove_lineto(node.value.red)
			node.value.top.unhilight()
			t.remove(p[event[i]])
			t.insert(trap)
			control.sleep ()

		p[event[i]].unhilight()
		control.sleep ()

	TriangMonotoneUsingDCEL(d)
	return 0