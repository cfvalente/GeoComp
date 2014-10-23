#!/usr/bin/env python
# -*- coding: utf-8 -*-
class edge():

	def __init__(self, origin, originInd, destiny):
		self.origin = origin
		self.originInd = originInd
		self.destiny = destiny
		self.next = None
		self.previous = None
		self.twin = None
		self.face = 0


class dcel():

	def __init__(self):
		self.faces = []


	def createDCELfromPolygon(self, p):
		n = len(p)


		ie = edge(p[0], 0, p[1])
		it = edge(p[1], 1, p[0])

		ie.face = 1
		it.face = 0

		ie.twin = it
		it.twin = ie

		e_aux = ie
		t_aux = it

		for i in range(1, n):

			e = edge(p[(i)%n], i, p[(i+1)%n])
			t = edge(p[(i+1)%n], (i+1)%n,  p[(i)%n])

			e.face = 1
			t.face = 0

			e.twin = t
			t.twin = e

			e_aux.next = e
			e.previous = e_aux

			t_aux.previous = t
			t.next = t_aux

			e_aux = e
			t_aux = t
			
		e.next = ie
		t.previous = it

		ie.previous = e
		it.next = t

		self.faces.append(it)
		self.faces.append(ie)

		return

	def printFaceVertices(self, i):
		origin = self.faces[i].origin
		print origin

		e = self.faces[i].next
		while(e.origin != origin):
			print e.origin
			e = e.next
		return

	def findFace(self, edge):
		for i in range(0, len(self.faces)):
			if(edge == self.faces[i]):
				return i
		origin = edge
		edge = edge.next
		while(edge != origin):
			for i in range(0, len(self.faces)):
				if(edge == self.faces[i]):
					return i
			edge = edge.next
		return -1

	def findEdgeUsingOrigin(self, point, face):
		e = self.faces[face]
		eo = e.origin
		if(e.origin == point):
			return e
		e = e.next
		while(e.origin != point):
			e = e.next
		return e

	# Nova aresta entre as origem da aresta1 ate a origem da aresta2
	def insertEdge(self, edge1, edge2):
		ne = edge(edge2.origin, edge2.originInd, edge1.origin)
		nt = edge(edge1.origin, edge1.originInd, edge2.origin)
		ne.twin = nt
		nt.twin = ne

		ne.next = edge1
		ne.previous = edge2.previous
		
		nt.next = edge2
		nt.previous = edge1.previous

		edge1.previous.next = nt
		edge1.previous = ne

		edge2.previous.next = ne
		edge2.previous = nt
		
		face = len(self.faces)

		ne.face = edge1.face
		nt.face = face

		nt_aux = nt.next
		while(nt != nt_aux):
			nt_aux.face = face
			nt_aux = nt_aux.next


		self.faces[edge1.face] = ne
		self.faces.append(nt)

		return ne