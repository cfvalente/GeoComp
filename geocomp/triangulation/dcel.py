class edge():

	def __init__(self, origin, destiny, face):
		self.origin = origin
		self.destiny = destiny
		self.next = None
		self.previous = None
		self.incidentFace = face #provavelmente nao sera necessario - verificar no algoritmo lee e preparata, basta guardar 1 das arestas de cada face, o que 'ja eh feito em dcel
		self.twin = None



class dcel():

	def __init__(self):
		self.faces = []


	def createDCELfromPolygon(self, p):
		n = len(p)


		ie = edge(p[0], p[1], 1)
		it = edge(p[1], p[0], -1)

		ie.twin = it
		it.twin = ie

		e_aux = ie
		t_aux = it

		for i in range(1, n):

			e = edge(p[(i)%n], p[(i+1)%n], 1)
			t = edge(p[(i+1)%n], p[(i)%n], -1)

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

	# Nova aresta entre as origem da aresta1 ate a origem da aresta2
	def insertEdge(self, edge1, edge2):
		ne = edge(edge2.origin, edge1.origin, edge1.incidentFace)
		nt = edge(edge1.origin, edge2.origin, len(self.faces))
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

		self.faces.append(nt)

		return