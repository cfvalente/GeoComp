from geocomp.common.prim import * 


def intersectsProp(a, b, c, d):
	if (collinear(a, b, c) or collinear(a, b, d) or collinear(c, d, a) or collinear(c, d, b)):
		return False
	return ((left(a, b, c) != left(a, b, d)) and (left(c, d, a) != left(c, d, b)))


def between(a, b, c):
	if( not collinear(a, b, c) ):
		return False
	if( a.x != b.x ):
		return ((a.x <= c.x and c.x <= b.x ) or ( b.x <= c.x <= a.x))
	return ((a.y <= c.y and c.y <= b.y ) or ( b.y <= c.y <= a.y))


def intersects(a, b, c, d):
	if intersectsProp(a, b, c, d):
		return True
	return (between(a, b, c) or between(a, b, d) or between(c, d, a) or between(c, d, b))


def inCone(n, p, i, j):
	u = (i-1)%n
	w = (i+1)%n
	if(left_on(p[u], p[i], p[w])):
		return (left(p[i], p[j], p[u]) and left(p[j], p[i], p[w]))
	return not ( left(p[i], p[j], p[w]) and left(p[j], p[i], p[u]) )


def almostDiagonal(n, p, i, j):
	for k in range(0, n):
		l = (k+1)%n
		if( k != i and k != j and l != i and l != j ):
			if(intersects(p[i], p[j], p[k], p[l])):
				return False
	return True


def isDiagonal(n, p, i, j):
	return ( inCone(n, p, i%n, j%n) and almostDiagonal(n, p, i%n, j%n) )


def isEar(n, p, i):
	return isDiagonal(n, p, (i-1)%n, (i+1)%n)


def findAllEars(n, p):
	ear = [False]*n
	for i in range(0, n):
		ear[i] = isEar(n, p, i)
	return ear


def Brute(p):
	print ""
	n = len(p)
	ear = findAllEars(n, p)
	while(n > 3):
		i = 0
		while ( not ear[i] ):
			i = i+1
		v2 = p[i]
		v1 = p[(i-1)%n]
		v3 = p[(i+1)%n]
		p.pop(i)
		ear.pop(i)
		n = n - 1
		indv1 = (i-1)%n
		indv3 = i%n
		ear[indv1] = isEar(n, p, indv1)
		ear[indv3] = isEar(n, p, indv3)
		print(str(v1)+" "+str(v3))
	return 0;